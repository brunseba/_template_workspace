#!/usr/bin/env python3
"""
Convert a single markdown file to DOCX using Pandoc.

This script allows you to convert individual markdown files to DOCX format,
with support for Mermaid diagrams and custom styling.
"""

import os
import sys
import tempfile
import subprocess
import re
import hashlib
from pathlib import Path


def check_pandoc():
    """Check if pandoc is available."""
    try:
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


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


def render_mermaid_to_png(mermaid_code, output_path, verbose=False):
    """Render Mermaid diagram to PNG using available mermaid-cli method"""
    available_methods = check_mermaid_cli_availability()
    
    if not available_methods:
        if verbose:
            print(f"    ⚠️  No mermaid-cli method available. Install Docker, Node.js/npm, or run: npm install -g @mermaid-js/mermaid-cli")
        return False
    
    # Try each available method
    for method in available_methods:
        try:
            if method == 'docker':
                return _render_with_docker(mermaid_code, output_path, verbose)
            elif method == 'npx':
                return _render_with_npx(mermaid_code, output_path, verbose)
            elif method == 'mmdc':
                return _render_with_mmdc(mermaid_code, output_path, verbose)
        except Exception as e:
            if verbose:
                print(f"    ⚠️  Failed to render with {method}: {e}")
            continue
    
    return False


def _render_with_docker(mermaid_code, output_path, verbose=False):
    """Render using Docker mermaid-cli"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as temp_mmd:
        temp_mmd.write(mermaid_code)
        temp_mmd_path = temp_mmd.name
    
    try:
        temp_dir = os.path.dirname(temp_mmd_path)
        temp_filename = os.path.basename(temp_mmd_path)
        output_filename = os.path.basename(output_path)
        
        docker_cmd = [
            'docker', 'run', '--rm',
            '-u', f"{os.getuid()}:{os.getgid()}",
            '-v', f"{temp_dir}:/data",
            'minlag/mermaid-cli',
            '-i', f"/data/{temp_filename}",
            '-o', f"/data/{output_filename}",
            '-b', 'white',
            '--scale', '2'
        ]
        
        result = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=60)
        temp_output_path = os.path.join(temp_dir, output_filename)
        
        if result.returncode == 0 and os.path.exists(temp_output_path):
            os.rename(temp_output_path, output_path)
            return True
        return False
    finally:
        if os.path.exists(temp_mmd_path):
            os.unlink(temp_mmd_path)


def _render_with_npx(mermaid_code, output_path, verbose=False):
    """Render using npx @mermaid-js/mermaid-cli"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as temp_mmd:
        temp_mmd.write(mermaid_code)
        temp_mmd_path = temp_mmd.name
    
    try:
        npx_cmd = [
            'npx', '-p', '@mermaid-js/mermaid-cli', 'mmdc',
            '-i', temp_mmd_path,
            '-o', output_path,
            '-b', 'white',
            '--scale', '2'
        ]
        
        result = subprocess.run(npx_cmd, capture_output=True, text=True, timeout=60)
        return result.returncode == 0 and os.path.exists(output_path)
    finally:
        if os.path.exists(temp_mmd_path):
            os.unlink(temp_mmd_path)


def _render_with_mmdc(mermaid_code, output_path, verbose=False):
    """Render using locally installed mmdc"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as temp_mmd:
        temp_mmd.write(mermaid_code)
        temp_mmd_path = temp_mmd.name
    
    try:
        mmdc_cmd = [
            'mmdc',
            '-i', temp_mmd_path,
            '-o', output_path,
            '-b', 'white',
            '--scale', '2'
        ]
        
        result = subprocess.run(mmdc_cmd, capture_output=True, text=True, timeout=60)
        return result.returncode == 0 and os.path.exists(output_path)
    finally:
        if os.path.exists(temp_mmd_path):
            os.unlink(temp_mmd_path)


def process_mermaid_diagrams(content, images_dir, verbose=False):
    """Process Mermaid diagrams in markdown content and render to images"""
    mermaid_pattern = r'```mermaid\n(.*?)\n```'
    
    def clean_mermaid_code(code):
        cleaned = code.rstrip('% \t\n\r')
        return cleaned.strip()
    
    diagram_count = 0
    successful_renders = 0
    
    def replace_mermaid(match):
        nonlocal diagram_count, successful_renders
        diagram_count += 1
        raw_mermaid_code = match.group(1)
        mermaid_code = clean_mermaid_code(raw_mermaid_code)
        
        diagram_hash = hashlib.md5(mermaid_code.encode('utf-8')).hexdigest()[:8]
        image_filename = f"mermaid_diagram_{diagram_count}_{diagram_hash}.png"
        image_path = os.path.join(images_dir, image_filename)
        
        # Determine diagram type
        if 'graph ' in mermaid_code or 'flowchart ' in mermaid_code:
            diagram_type = "Flowchart"
        elif 'sequenceDiagram' in mermaid_code:
            diagram_type = "Sequence Diagram"
        elif 'gantt' in mermaid_code:
            diagram_type = "Gantt Chart"
        elif 'pie' in mermaid_code:
            diagram_type = "Pie Chart"
        elif 'classDiagram' in mermaid_code:
            diagram_type = "Class Diagram"
        elif 'erDiagram' in mermaid_code:
            diagram_type = "ER Diagram"
        else:
            diagram_type = "Diagram"
        
        if verbose:
            print(f"    🎨 Rendering {diagram_type}...")
        
        if render_mermaid_to_png(mermaid_code, image_path, verbose):
            successful_renders += 1
            replacement = f"\n**{diagram_type}**\n\n![{diagram_type}]({image_path})\n\n"
        else:
            # Fallback to code block if rendering fails
            replacement = f"\n**[Mermaid {diagram_type} - Rendering Failed]**\n\n"
            replacement += f"```\n{mermaid_code}\n```\n"
            replacement += "\n*Note: Diagram rendering failed, showing code instead.*\n\n"
        
        return replacement
    
    processed_content = re.sub(mermaid_pattern, replace_mermaid, content, flags=re.DOTALL)
    
    if diagram_count > 0 and verbose:
        print(f"  → Processed {diagram_count} Mermaid diagram(s) ({successful_renders} rendered successfully)")
    
    return processed_content


def convert_single_file(input_file, output_file=None, title=None, include_toc=True, verbose=False):
    """
    Convert a single markdown file to DOCX.
    
    Args:
        input_file: Path to input markdown file
        output_file: Path to output DOCX file (optional, auto-generated if not provided)
        title: Document title (optional, uses filename if not provided)
        include_toc: Include table of contents (default: True)
        verbose: Enable verbose output (default: False)
    
    Returns:
        0 on success, 1 on failure
    """
    # Validate input file
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_file}")
        return 1
    
    if not input_path.is_file():
        print(f"Error: Input path is not a file: {input_file}")
        return 1
    
    # Generate output filename if not provided
    if output_file is None:
        output_file = input_path.with_suffix('.docx').name
        # Place in docs/export if it exists, otherwise current directory
        if Path('docs/export').exists():
            output_file = f'docs/export/{output_file}'
    
    output_path = Path(output_file)
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate title if not provided
    if title is None:
        title = input_path.stem.replace('-', ' ').replace('_', ' ').title()
    
    if verbose:
        print(f"Converting: {input_path}")
        print(f"Output: {output_path}")
        print(f"Title: {title}")
    
    # Read input file
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create temporary directory for Mermaid images
    temp_images_dir = tempfile.mkdtemp(prefix='mermaid_images_')
    
    # Process Mermaid diagrams
    if '```mermaid' in content:
        if verbose:
            print(f"Processing Mermaid diagrams...")
            print(f"Images will be saved to: {temp_images_dir}")
        content = process_mermaid_diagrams(content, temp_images_dir, verbose)
    
    # Create temporary markdown file with processed content
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_md:
        temp_md.write(content)
        temp_md_path = temp_md.name
    
    # Build pandoc command
    cmd = [
        'pandoc',
        temp_md_path,
        '-o', str(output_path),
        '--from', 'markdown+fenced_code_blocks+fenced_code_attributes+backtick_code_blocks',
        '--to', 'docx',
        '--standalone',
        '--number-sections',
        '--syntax-highlighting=pygments',
        '--metadata', f'title={title}',
        '--metadata', 'author=Documentation Team',
    ]
    
    # Add date metadata
    try:
        date = subprocess.check_output(['date', '+%Y-%m-%d'], text=True).strip()
        cmd.extend(['--metadata', f'date={date}'])
    except:
        pass
    
    # Add TOC if enabled
    if include_toc:
        cmd.extend(['--toc', '--toc-depth=3'])
    
    # Add reference doc if it exists
    reference_doc_paths = [
        'scripts/reference.docx',
        '../scripts/reference.docx',
        '../../scripts/reference.docx',
    ]
    
    for ref_path in reference_doc_paths:
        if Path(ref_path).exists():
            cmd.extend(['--reference-doc', ref_path])
            if verbose:
                print(f"Using reference document: {ref_path}")
            break
    
    if verbose:
        print(f"Running: {' '.join(cmd)}")
    
    # Run pandoc
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        if verbose and result.stderr:
            print(f"Pandoc output: {result.stderr}")
        
        print(f"✅ Success! DOCX file created: {output_path}")
        
        # Show file size
        file_size = output_path.stat().st_size
        if file_size < 1024:
            size_str = f"{file_size} bytes"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size / 1024 / 1024:.1f} MB"
        
        print(f"📄 File size: {size_str}")
        
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"Error: Conversion failed with exit code {e.returncode}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1
    finally:
        # Clean up temporary files
        if os.path.exists(temp_md_path):
            os.unlink(temp_md_path)


def main(input_file, output_file=None, title=None, include_toc=True, verbose=False):
    """Main entry point."""
    # Check dependencies
    if not check_pandoc():
        print("Error: pandoc is not installed or not available in PATH")
        print("Install pandoc: https://pandoc.org/installing.html")
        return 1
    
    return convert_single_file(
        input_file=input_file,
        output_file=output_file,
        title=title,
        include_toc=include_toc,
        verbose=verbose
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_single_file.py <input.md> [output.docx]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    sys.exit(main(input_file, output_file))
