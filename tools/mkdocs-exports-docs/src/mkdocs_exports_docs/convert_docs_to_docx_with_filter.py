#!/usr/bin/env python3
"""
Convert MkDocs documentation to DOCX using pandoc-mermaid-filter.

This script provides an alternative approach to the main conversion script,
using pandoc-mermaid-filter for native Mermaid diagram rendering.

Requirements:
- pandoc
- pandoc-mermaid-filter (npm install -g @mermaid-js/mermaid-cli pandoc-mermaid-filter)
- Python packages: PyYAML, pathlib
"""

import os
import sys
import yaml
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Any
import tempfile
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class MkDocsToDocxConverter:
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
    
    def combine_markdown_files(self, files: List[Path]) -> str:
        """Combine multiple markdown files into a single document."""
        combined_content = []
        
        for i, file_path in enumerate(files):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Add page break before each section (except first)
                if i > 0:
                    combined_content.append('\n\\newpage\n')
                
                # Add file title as a heading
                relative_path = file_path.relative_to(self.docs_dir)
                section_title = f"# {relative_path.stem.replace('-', ' ').replace('_', ' ').title()}"
                combined_content.append(section_title)
                combined_content.append('')
                
                # Adjust heading levels in content (shift all headings down by 1)
                adjusted_content = self.adjust_heading_levels(content, 1)
                combined_content.append(adjusted_content)
                combined_content.append('')
                
                logger.info(f"Added: {relative_path}")
                
            except Exception as e:
                logger.error(f"Failed to read {file_path}: {e}")
                
        return '\n'.join(combined_content)
    
    def convert_to_docx(self, markdown_content: str, output_file: Path) -> bool:
        """Convert markdown content to DOCX using pandoc with mermaid filter."""
        
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
                '--metadata', 'title=Complete Documentation',
                '--metadata', 'author=Documentation Team',
                '--metadata', 'date=' + subprocess.run(['date', '+%Y-%m-%d'], capture_output=True, text=True).stdout.strip()
            ]
            
            # Remove empty reference-doc argument if file doesn't exist
            pandoc_cmd = [arg for arg in pandoc_cmd if arg and not arg.startswith('--reference-doc=--reference-doc')]
            
            logger.info(f"Running pandoc with mermaid filter...")
            logger.debug(f"Command: {' '.join(pandoc_cmd)}")
            
            result = subprocess.run(
                pandoc_cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode == 0:
                logger.info(f"✓ Successfully created DOCX: {output_file}")
                logger.info(f"File size: {output_file.stat().st_size / 1024 / 1024:.2f} MB")
                return True
            else:
                logger.error(f"Pandoc failed with return code {result.returncode}")
                logger.error(f"STDOUT: {result.stdout}")
                logger.error(f"STDERR: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Pandoc conversion timed out after 5 minutes")
            return False
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            return False
        finally:
            # Clean up temporary file
            tmp_markdown.unlink(missing_ok=True)
    
    def run(self) -> bool:
        """Run the complete conversion process."""
        logger.info("Starting MkDocs to DOCX conversion with pandoc-mermaid-filter")
        
        # Check dependencies
        if not self.check_dependencies():
            return False
            
        # Load MkDocs configuration
        config = self.load_mkdocs_config()
        if not config:
            logger.error("Failed to load MkDocs configuration")
            return False
            
        # Extract navigation files
        nav = config.get('nav', [])
        if not nav:
            logger.error("No navigation found in MkDocs config")
            return False
            
        files = self.extract_nav_files(nav)
        if not files:
            logger.error("No files found in navigation")
            return False
            
        logger.info(f"Found {len(files)} files to process")
        
        # Combine markdown files
        logger.info("Combining markdown files...")
        combined_content = self.combine_markdown_files(files)
        
        if not combined_content.strip():
            logger.error("No content to convert")
            return False
            
        # Convert to DOCX
        output_file = self.export_dir / "Complete_Documentation_Filtered.docx"
        logger.info(f"Converting to DOCX: {output_file}")
        
        success = self.convert_to_docx(combined_content, output_file)
        
        if success:
            logger.info("✓ Conversion completed successfully!")
            logger.info(f"Output file: {output_file}")
        else:
            logger.error("✗ Conversion failed!")
            
        return success

def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    converter = MkDocsToDocxConverter(project_root)
    success = converter.run()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
