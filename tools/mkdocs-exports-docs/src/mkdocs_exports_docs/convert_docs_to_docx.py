#!/usr/bin/env python3
"""
Convert MkDocs documentation to a comprehensive DOCX file using Pandoc
"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path
import yaml
from yaml import SafeLoader
import re
import hashlib
import base64
import json
import requests
import urllib.parse

# Custom YAML loader to handle MkDocs-specific Python tags
class MkDocsYamlLoader(SafeLoader):
    """Custom YAML loader that can handle MkDocs Python function references"""
    pass

# Add constructor for Python function references
def python_name_constructor(loader, node):
    """Handle !!python/name: tags by returning a placeholder string"""
    if hasattr(node, 'value'):
        return f"<python_function:{node.value}>"
    else:
        return "<python_function:unknown>"

# Add constructor for the specific tag format that MkDocs uses
MkDocsYamlLoader.add_constructor('tag:yaml.org,2002:python/name:pymdownx.superfences.fence_code_format', 
                                 lambda loader, node: "<mermaid_formatter>")

# Add generic constructor for any python/name tags
MkDocsYamlLoader.add_multi_constructor('tag:yaml.org,2002:python/name:', python_name_constructor)

def check_mermaid_cli_availability():
    """Check if mermaid-cli is available via different methods"""
    methods = []
    
    # Check Docker
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            # Check if docker daemon is running
            result = subprocess.run(['docker', 'info'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                methods.append('docker')
    except:
        pass
    
    # Check npx
    try:
        result = subprocess.run(['npx', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            methods.append('npx')
    except:
        pass
    
    # Check locally installed mmdc
    try:
        result = subprocess.run(['mmdc', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            methods.append('mmdc')
    except:
        pass
    
    return methods

def render_mermaid_to_png(mermaid_code, output_path):
    """Render Mermaid diagram to PNG using available mermaid-cli method"""
    available_methods = check_mermaid_cli_availability()
    
    if not available_methods:
        print(f"    ⚠️ No mermaid-cli method available. Install Docker, Node.js/npm, or run: npm install -g @mermaid-js/mermaid-cli")
        return False
    
    # Try each available method
    for method in available_methods:
        try:
            if method == 'docker':
                return _render_with_docker(mermaid_code, output_path)
            elif method == 'npx':
                return _render_with_npx(mermaid_code, output_path)
            elif method == 'mmdc':
                return _render_with_mmdc(mermaid_code, output_path)
        except Exception as e:
            print(f"    ⚠️ Failed to render with {method}: {e}")
            continue
    
    return False

def _render_with_docker(mermaid_code, output_path):
    """Render using Docker mermaid-cli"""
    # Create temporary mermaid file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as temp_mmd:
        temp_mmd.write(mermaid_code)
        temp_mmd_path = temp_mmd.name
    
    try:
        # Get directory paths for Docker volume mounting
        temp_dir = os.path.dirname(temp_mmd_path)
        temp_filename = os.path.basename(temp_mmd_path)
        output_filename = os.path.basename(output_path)
        
        # Docker command to run mermaid-cli
        docker_cmd = [
            'docker', 'run', '--rm',
            '-u', f"{os.getuid()}:{os.getgid()}",
            '-v', f"{temp_dir}:/data",
            'minlag/mermaid-cli',
            '-i', f"/data/{temp_filename}",
            '-o', f"/data/{output_filename}",
            '-b', 'white',  # white background
            '--scale', '2'  # higher resolution
        ]
        
        # Run docker command
        result = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=60)
        
        # Check if file was created in temp directory
        temp_output_path = os.path.join(temp_dir, output_filename)
        
        # Debug: Print command output
        if result.stdout.strip():
            print(f"    📝 Docker stdout: {result.stdout.strip()}")
        if result.stderr.strip():
            print(f"    ⚠️ Docker stderr: {result.stderr.strip()}")
        
        if result.returncode == 0:
            if os.path.exists(temp_output_path):
                # Move the generated file to the desired location
                os.rename(temp_output_path, output_path)
                return True
            else:
                # File not created - this indicates a rendering failure
                print(f"    ⚠️ Docker succeeded but no output file created (likely syntax error)")
                return False
        else:
            # Docker failed
            stderr_msg = result.stderr.strip() if result.stderr.strip() else "Unknown error"
            print(f"    ⚠️ Docker command failed (code {result.returncode}): {stderr_msg}")
            return False
    finally:
        if os.path.exists(temp_mmd_path):
            os.unlink(temp_mmd_path)

def _render_with_npx(mermaid_code, output_path):
    """Render using npx @mermaid-js/mermaid-cli"""
    # Create temporary mermaid file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as temp_mmd:
        temp_mmd.write(mermaid_code)
        temp_mmd_path = temp_mmd.name
    
    try:
        # npx command to run mermaid-cli
        npx_cmd = [
            'npx', '-p', '@mermaid-js/mermaid-cli', 'mmdc',
            '-i', temp_mmd_path,
            '-o', output_path,
            '-b', 'white',
            '--scale', '2'
        ]
        
        # Run npx command
        result = subprocess.run(npx_cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and os.path.exists(output_path):
            return True
        else:
            print(f"    ⚠️ npx command failed: {result.stderr}")
            return False
    finally:
        if os.path.exists(temp_mmd_path):
            os.unlink(temp_mmd_path)

def _render_with_mmdc(mermaid_code, output_path):
    """Render using locally installed mmdc"""
    # Create temporary mermaid file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as temp_mmd:
        temp_mmd.write(mermaid_code)
        temp_mmd_path = temp_mmd.name
    
    try:
        # mmdc command
        mmdc_cmd = [
            'mmdc',
            '-i', temp_mmd_path,
            '-o', output_path,
            '-b', 'white',
            '--scale', '2'
        ]
        
        # Run mmdc command
        result = subprocess.run(mmdc_cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and os.path.exists(output_path):
            return True
        else:
            print(f"    ⚠️ mmdc command failed: {result.stderr}")
            return False
    finally:
        if os.path.exists(temp_mmd_path):
            os.unlink(temp_mmd_path)

def load_mkdocs_config():
    """Load MkDocs configuration using custom loader"""
    with open('mkdocs.yml', 'r') as f:
        return yaml.load(f, Loader=MkDocsYamlLoader)

def process_mermaid_diagrams(content, images_dir):
    """Process Mermaid diagrams in markdown content and render to images"""
    # Pattern to match mermaid code blocks
    mermaid_pattern = r'```mermaid\n(.*?)\n```'
    
    # Fix: Remove trailing % character and other problematic characters causing syntax errors
    def clean_mermaid_code(code):
        # Remove trailing % and excessive whitespace, but preserve necessary whitespace
        cleaned = code.rstrip('% \t\n\r')
        return cleaned.strip()
    
    # Count diagrams processed
    diagram_count = 0
    successful_renders = 0
    
    def replace_mermaid(match):
        nonlocal diagram_count, successful_renders
        diagram_count += 1
        raw_mermaid_code = match.group(1)
        mermaid_code = clean_mermaid_code(raw_mermaid_code)
        
        # Create a unique filename for this diagram based on cleaned code
        diagram_hash = hashlib.md5(mermaid_code.encode('utf-8')).hexdigest()[:8]
        image_filename = f"mermaid_diagram_{diagram_count}_{diagram_hash}.png"
        image_path = os.path.join(images_dir, image_filename)
        
        # Analyze the mermaid code to provide a description
        if 'graph ' in mermaid_code or 'flowchart ' in mermaid_code:
            diagram_type = "Flowchart/Graph Diagram"
        elif 'sequenceDiagram' in mermaid_code:
            diagram_type = "Sequence Diagram"
        elif 'gantt' in mermaid_code:
            diagram_type = "Gantt Chart"
        elif 'pie' in mermaid_code:
            diagram_type = "Pie Chart"
        elif 'classDiagram' in mermaid_code:
            diagram_type = "Class Diagram"
        elif 'erDiagram' in mermaid_code:
            diagram_type = "Entity Relationship Diagram"
        elif 'journey' in mermaid_code:
            diagram_type = "User Journey Diagram"
        else:
            diagram_type = "Diagram"
        
        # Try to render the diagram to PNG
        print(f"    🎨 Rendering {diagram_type}...")
        
        # Debug: print the first few lines of mermaid code
        code_lines = mermaid_code.strip().split('\n')
        print(f"    🔍 Code preview: {code_lines[0] if code_lines else 'empty'}...")
        
        if render_mermaid_to_png(mermaid_code, image_path):
            successful_renders += 1
            # Create markdown image reference
            replacement = f"\n**{diagram_type}**\n\n![{diagram_type}]({image_path})\n\n"
        else:
            # Save failed diagram to debug file
            debug_filename = f"failed_mermaid_{diagram_count}_{diagram_hash}.mmd"
            debug_path = os.path.join(images_dir, debug_filename)
            with open(debug_path, 'w', encoding='utf-8') as debug_file:
                debug_file.write(mermaid_code)
            print(f"    💾 Saved failing diagram to: {debug_path}")
            
            # Fallback to text description if rendering fails
            replacement = f"\n**[Mermaid {diagram_type} - Rendering Failed]**\n\n"
            replacement += f"```\n{mermaid_code}\n```\n"
            replacement += "\n*Note: Diagram rendering failed, showing code instead.*\n\n"
        
        return replacement
    
    # Replace all mermaid blocks
    processed_content = re.sub(mermaid_pattern, replace_mermaid, content, flags=re.DOTALL)
    
    if diagram_count > 0:
        print(f"  → Processed {diagram_count} Mermaid diagram(s) ({successful_renders} rendered successfully)")
    
    return processed_content

def extract_nav_files(nav_section, prefix=""):
    """Recursively extract markdown files from navigation structure"""
    files = []
    
    if isinstance(nav_section, list):
        for item in nav_section:
            files.extend(extract_nav_files(item, prefix))
    elif isinstance(nav_section, dict):
        for key, value in nav_section.items():
            if isinstance(value, str):
                # This is a file
                file_path = f"docs/{value}"
                if os.path.exists(file_path):
                    files.append((key, file_path))
                else:
                    print(f"Warning: File {file_path} not found")
            elif isinstance(value, (list, dict)):
                # This is a section
                files.extend(extract_nav_files(value, f"{prefix}{key} - " if prefix else f"{key} - "))
    
    return files

def create_combined_markdown(files, output_path, images_dir):
    """Combine all markdown files into one document"""
    
    with open(output_path, 'w', encoding='utf-8') as combined:
        # Write title page
        combined.write("# Complete Documentation\n\n")
        combined.write("## Documentation Export\n\n")
        combined.write("*Generated from MkDocs documentation*\n\n")
        combined.write("---\n\n")
        
        # Write table of contents
        combined.write("# Table of Contents\n\n")
        for title, _ in files:
            # Create anchor-friendly title
            anchor = title.lower().replace(' ', '-').replace('&', 'and')
            combined.write(f"- [{title}](#{anchor})\n")
        combined.write("\n---\n\n")
        
        # Process each file
        for title, file_path in files:
            print(f"Processing: {title} -> {file_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Add section header
                combined.write(f"\n\\newpage\n\n# {title}\n\n")
                
                # Process mermaid diagrams
                content = process_mermaid_diagrams(content, images_dir)
                
                # Process content to adjust heading levels
                lines = content.split('\n')
                processed_lines = []
                
                for line in lines:
                    # Adjust heading levels (add one # to make them sub-sections)
                    if line.startswith('#'):
                        line = '#' + line
                    processed_lines.append(line)
                
                # Write processed content
                combined.write('\n'.join(processed_lines))
                combined.write('\n\n')
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                combined.write(f"*Error loading content from {file_path}*\n\n")

def convert_to_docx(markdown_path, docx_path):
    """Convert markdown to DOCX using Pandoc"""
    
    # Pandoc command with comprehensive options
    cmd = [
        'pandoc',
        markdown_path,
        '-o', docx_path,
        '--from', 'markdown+fenced_code_blocks+fenced_code_attributes+backtick_code_blocks',
        '--to', 'docx',
        '--toc',
        '--toc-depth=3',
        '--number-sections',
        '--highlight-style', 'pygments',
        '--metadata', 'title=Complete Documentation',
        '--metadata', 'author=Documentation Team',
        '--metadata', 'date=' + subprocess.check_output(['date', '+%Y-%m-%d']).decode().strip(),
    ]
    
    # Add reference doc if it exists
    if os.path.exists('scripts/reference.docx'):
        cmd.extend(['--reference-doc', 'scripts/reference.docx'])
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Conversion successful!")
        if result.stderr:
            print(f"Warnings: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed: {e}")
        print(f"Error output: {e.stderr}")
        raise

def main():
    """Main conversion process"""
    
    # Change to project root if we're in scripts directory
    if os.path.basename(os.getcwd()) == 'scripts':
        os.chdir('..')
    
    # Check if we're in the right directory
    if not os.path.exists('mkdocs.yml'):
        print("Error: mkdocs.yml not found. Run this script from the project root or scripts directory.")
        return 1
    
    # Load MkDocs configuration
    print("Loading MkDocs configuration...")
    config = load_mkdocs_config()
    
    # Extract files from navigation
    print("Extracting files from navigation...")
    nav_files = extract_nav_files(config.get('nav', []))
    
    print(f"Found {len(nav_files)} files to process")
    
    # Create temporary directories for images
    temp_images_dir = tempfile.mkdtemp(prefix='mermaid_images_')
    
    # Create temporary combined markdown file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_md:
        temp_md_path = temp_md.name
    
    try:
        # Combine all markdown files
        print("Combining markdown files...")
        print(f"Images will be saved to: {temp_images_dir}")
        create_combined_markdown(nav_files, temp_md_path, temp_images_dir)
        
        # Convert to DOCX
        output_path = 'docs/export/Complete_Documentation.docx'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        print(f"Converting to DOCX: {output_path}")
        convert_to_docx(temp_md_path, output_path)
        
        print(f"\n✅ Success! DOCX file created: {output_path}")
        print(f"📄 File size: {os.path.getsize(output_path)} bytes")
        
        return 0
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_md_path):
            os.unlink(temp_md_path)

if __name__ == "__main__":
    exit(main())
