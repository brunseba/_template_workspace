#!/usr/bin/env python3
"""
Convert MkDocs documentation to separate DOCX files by chapter using pandoc-mermaid-filter.

This script creates individual DOCX files for each major chapter of the documentation,
making it easier to distribute and work with specific sections.

Requirements:
- pandoc
- mermaid-filter (npm install -g @mermaid-js/mermaid-cli mermaid-filter)
- Python packages: PyYAML, pathlib
"""

import os
import sys
import yaml
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Any, Tuple
import tempfile
import logging
import re

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class MkDocsToDocxByChapterConverter:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.docs_dir = project_root / "docs"
        self.export_dir = project_root / "docs" / "export"
        self.mkdocs_config = project_root / "mkdocs.yml"
        
        # Ensure export directory exists
        self.export_dir.mkdir(exist_ok=True)
        
    def check_dependencies(self) -> bool:
        """Check if required dependencies are available."""
        dependencies = ['pandoc', 'mermaid-filter']
        
        missing = []
        for dep in dependencies:
            try:
                result = subprocess.run(['which', dep], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=10)
                if result.returncode != 0:
                    missing.append(dep)
                else:
                    logger.info(f"✓ {dep} is available at {result.stdout.strip()}")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                missing.append(dep)
        
        if missing:
            logger.error(f"Missing dependencies: {', '.join(missing)}")
            logger.error("Install with: npm install -g @mermaid-js/mermaid-cli mermaid-filter")
            return False
            
        return True
    
    def load_mkdocs_config(self) -> Dict[str, Any]:
        """Load and parse MkDocs configuration."""
        class SafeLoaderIgnoreTags(yaml.SafeLoader):
            def ignore_unknown(self, node):
                return None
        
        SafeLoaderIgnoreTags.add_constructor(None, SafeLoaderIgnoreTags.ignore_unknown)
        
        try:
            with open(self.mkdocs_config, 'r', encoding='utf-8') as f:
                config = yaml.load(f, Loader=SafeLoaderIgnoreTags)
                logger.info(f"Loaded MkDocs config: {self.mkdocs_config}")
                return config
        except Exception as e:
            logger.error(f"Failed to load MkDocs config: {e}")
            return {}
    
    def extract_chapters_from_nav(self, nav: List[Any]) -> Dict[str, List[Path]]:
        """Extract chapters and their files from navigation structure."""
        chapters = {}
        
        for item in nav:
            if isinstance(item, dict):
                for chapter_name, chapter_content in item.items():
                    # Clean chapter name for filename
                    clean_name = re.sub(r'[^\w\s-]', '', chapter_name).strip()
                    clean_name = re.sub(r'[-\s]+', '-', clean_name)
                    
                    files = self.extract_nav_files(chapter_content)
                    if files:
                        chapters[clean_name] = files
                        logger.info(f"Chapter '{chapter_name}': {len(files)} files")
            elif isinstance(item, str):
                # This is a top-level file (like index.md)
                file_path = self.docs_dir / item
                if file_path.exists():
                    chapters["Home"] = [file_path]
                    
        return chapters
    
    def extract_nav_files(self, nav_item, base_path: Path = None) -> List[Path]:
        """Recursively extract file paths from navigation structure."""
        files = []
        
        if base_path is None:
            base_path = self.docs_dir
            
        if isinstance(nav_item, dict):
            for key, value in nav_item.items():
                files.extend(self.extract_nav_files(value, base_path))
        elif isinstance(nav_item, list):
            for item in nav_item:
                files.extend(self.extract_nav_files(item, base_path))
        elif isinstance(nav_item, str):
            # This is a file path
            file_path = base_path / nav_item
            if file_path.exists():
                files.append(file_path)
            else:
                logger.warning(f"File not found: {file_path}")
                
        return files
    
    def adjust_heading_levels(self, content: str, level_adjustment: int = 0) -> str:
        """Adjust markdown heading levels."""
        if level_adjustment == 0:
            return content
            
        lines = content.split('\n')
        adjusted_lines = []
        
        for line in lines:
            if line.startswith('#'):
                # Count current heading level
                current_level = 0
                for char in line:
                    if char == '#':
                        current_level += 1
                    else:
                        break
                
                # Extract heading text
                heading_text = line[current_level:].strip()
                
                # Calculate new level (minimum 1, maximum 6)
                new_level = max(1, min(6, current_level + level_adjustment))
                
                # Create new heading
                new_heading = '#' * new_level + ' ' + heading_text
                adjusted_lines.append(new_heading)
            else:
                adjusted_lines.append(line)
                
        return '\n'.join(adjusted_lines)
    
    def combine_chapter_files(self, chapter_name: str, files: List[Path]) -> str:
        """Combine multiple markdown files for a chapter into a single document."""
        combined_content = []
        
        # Add chapter title
        chapter_title = f"# {chapter_name.replace('-', ' ').title()}"
        combined_content.append(chapter_title)
        combined_content.append('')
        
        for i, file_path in enumerate(files):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Add section break before each file (except first)
                if i > 0:
                    combined_content.append('\n\\newpage\n')
                
                # Add file title as a section heading
                relative_path = file_path.relative_to(self.docs_dir)
                section_title = f"## {relative_path.stem.replace('-', ' ').replace('_', ' ').title()}"
                combined_content.append(section_title)
                combined_content.append('')
                
                # Adjust heading levels in content (shift all headings down by 2)
                adjusted_content = self.adjust_heading_levels(content, 2)
                combined_content.append(adjusted_content)
                combined_content.append('')
                
                logger.debug(f"Added to {chapter_name}: {relative_path}")
                
            except Exception as e:
                logger.error(f"Failed to read {file_path}: {e}")
                
        return '\n'.join(combined_content)
    
    def convert_to_docx(self, chapter_name: str, markdown_content: str) -> bool:
        """Convert markdown content to DOCX using pandoc with mermaid filter."""
        
        # Create output filename
        output_file = self.export_dir / f"{chapter_name}_Documentation.docx"
        
        # Create temporary markdown file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp_file:
            tmp_file.write(markdown_content)
            tmp_markdown = Path(tmp_file.name)
        
        try:
            # Pandoc command with mermaid filter
            pandoc_cmd = [
                'pandoc',
                str(tmp_markdown),
                '--filter', 'mermaid-filter',
                '--from', 'markdown',
                '--to', 'docx',
                '--output', str(output_file),
                '--toc',
                '--toc-depth=3',
                '--standalone',
                '--reference-doc=' + str(self.project_root / 'scripts' / 'reference.docx') if (self.project_root / 'scripts' / 'reference.docx').exists() else '',
                '--metadata', f'title={chapter_name.replace("-", " ").title()} Documentation',
                '--metadata', 'author=Documentation Team',
                '--metadata', 'date=' + subprocess.run(['date', '+%Y-%m-%d'], capture_output=True, text=True).stdout.strip()
            ]
            
            # Remove empty reference-doc argument if file doesn't exist
            pandoc_cmd = [arg for arg in pandoc_cmd if arg and not arg.startswith('--reference-doc=--reference-doc')]
            
            logger.info(f"Converting {chapter_name} to DOCX...")
            
            result = subprocess.run(
                pandoc_cmd,
                capture_output=True,
                text=True,
                timeout=120  # 2 minutes timeout per chapter
            )
            
            if result.returncode == 0:
                file_size = output_file.stat().st_size / 1024 / 1024
                logger.info(f"✓ Created {output_file.name} ({file_size:.2f} MB)")
                return True
            else:
                logger.error(f"Pandoc failed for {chapter_name} with return code {result.returncode}")
                logger.error(f"STDERR: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"Pandoc conversion timed out for {chapter_name}")
            return False
        except Exception as e:
            logger.error(f"Conversion failed for {chapter_name}: {e}")
            return False
        finally:
            # Clean up temporary file
            tmp_markdown.unlink(missing_ok=True)
    
    def run(self) -> bool:
        """Run the complete conversion process."""
        logger.info("Starting MkDocs to DOCX conversion by chapter with pandoc-mermaid-filter")
        
        # Check dependencies
        if not self.check_dependencies():
            return False
            
        # Load MkDocs configuration
        config = self.load_mkdocs_config()
        if not config:
            logger.error("Failed to load MkDocs configuration")
            return False
            
        # Extract navigation structure
        nav = config.get('nav', [])
        if not nav:
            logger.error("No navigation found in MkDocs config")
            return False
            
        # Extract chapters
        chapters = self.extract_chapters_from_nav(nav)
        if not chapters:
            logger.error("No chapters found in navigation")
            return False
            
        logger.info(f"Found {len(chapters)} chapters to process")
        
        # Process each chapter
        success_count = 0
        failed_chapters = []
        
        for chapter_name, files in chapters.items():
            logger.info(f"Processing chapter: {chapter_name} ({len(files)} files)")
            
            # Combine files for this chapter
            combined_content = self.combine_chapter_files(chapter_name, files)
            
            if not combined_content.strip():
                logger.warning(f"No content for chapter: {chapter_name}")
                continue
                
            # Convert to DOCX
            if self.convert_to_docx(chapter_name, combined_content):
                success_count += 1
            else:
                failed_chapters.append(chapter_name)
        
        # Summary
        logger.info(f"✓ Successfully converted {success_count} chapters")
        if failed_chapters:
            logger.error(f"✗ Failed to convert {len(failed_chapters)} chapters: {', '.join(failed_chapters)}")
            
        logger.info(f"Output directory: {self.export_dir}")
        return len(failed_chapters) == 0

def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    converter = MkDocsToDocxByChapterConverter(project_root)
    success = converter.run()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
