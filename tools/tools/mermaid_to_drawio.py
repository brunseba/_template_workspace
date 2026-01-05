#!/usr/bin/env python3
"""
Command-line tool to generate Draw.io files from Mermaid diagrams
Usage: python3 mermaid_to_drawio.py [input_directory] [output_file]
"""

import json
import html
import os
import uuid
import glob
import argparse
import sys
from pathlib import Path
from typing import List, Dict

def escape_for_xml(text: str) -> str:
    """Escape text for XML attributes, including JSON content"""
    # First escape HTML entities
    escaped = html.escape(text, quote=True)
    # Replace newlines with \n for JSON strings
    escaped = escaped.replace('\n', '\\n')
    return escaped

def create_mermaid_data_json(mermaid_content: str) -> str:
    """Create the JSON structure for mermaidData attribute"""
    mermaid_data = {
        "data": mermaid_content.strip()
    }
    return json.dumps(mermaid_data, separators=(',', ':'))

def generate_unique_id() -> str:
    """Generate a unique ID for diagram elements"""
    return str(uuid.uuid4()).replace('-', '')[:16]

def get_diagram_name_from_filename(filename: str) -> str:
    """Extract a clean diagram name from filename"""
    # Remove .mmd extension
    name = filename.replace('.mmd', '')
    # Remove common prefixes
    name = name.replace('mermaid-example_', '')
    name = name.replace('example_', '')
    # Replace underscores with spaces and capitalize
    name = name.replace('_', ' ').replace('-', ' ')
    return name.title()

def create_diagram_element(mermaid_content: str, diagram_name: str, diagram_id: str) -> str:
    """Create a diagram element with proper XML structure"""
    
    # Create the mermaidData JSON and escape it for XML
    mermaid_json = create_mermaid_data_json(mermaid_content)
    escaped_mermaid_data = escape_for_xml(mermaid_json)
    
    # Generate unique IDs for the UserObject and mxCell
    user_object_id = generate_unique_id()
    
    # Create the diagram XML structure
    diagram_xml = f'''  <diagram id="{diagram_id}" name="{diagram_name}">
    <mxGraphModel dx="706" dy="604" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <UserObject label="" mermaidData="{escaped_mermaid_data}" id="{user_object_id}">
          <mxCell style="shape=image;noLabel=1;verticalAlign=top;imageAspect=1;image=data:image/svg+xml,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iI2Y5ZjlmOSIgc3Ryb2tlPSIjY2NjIi8+PHRleHQgeD0iMTAwIiB5PSIxMDAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzMzMyI+TWVybWFpZCBEaWFncmFtPC90ZXh0Pjwvc3ZnPg==;" vertex="1" parent="1">
            <mxGeometry x="260" y="130" width="200" height="200" as="geometry" />
          </mxCell>
        </UserObject>
      </root>
    </mxGraphModel>
  </diagram>'''
    
    return diagram_xml

def generate_drawio_file(mermaid_files: List[str], output_file: str, verbose: bool = False) -> None:
    """Generate a Draw.io file from multiple Mermaid files"""
    
    diagrams = []
    
    for mermaid_file in mermaid_files:
        if not os.path.exists(mermaid_file):
            if verbose:
                print(f"Warning: File {mermaid_file} not found, skipping...")
            continue
            
        # Read the Mermaid content
        try:
            with open(mermaid_file, 'r', encoding='utf-8') as f:
                mermaid_content = f.read()
        except Exception as e:
            if verbose:
                print(f"Error reading {mermaid_file}: {e}")
            continue
        
        # Generate diagram name and ID
        filename = os.path.basename(mermaid_file)
        diagram_name = get_diagram_name_from_filename(filename)
        diagram_id = generate_unique_id()
        
        if verbose:
            print(f"Processing: {filename} -> {diagram_name}")
        
        # Create the diagram element
        diagram_xml = create_diagram_element(mermaid_content, diagram_name, diagram_id)
        diagrams.append(diagram_xml)
    
    if not diagrams:
        print("No valid Mermaid files found!")
        return
    
    # Create the complete Draw.io file
    pages_count = len(diagrams)
    
    drawio_content = f'''<mxfile host="Electron" agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) draw.io/28.0.4 Chrome/138.0.7204.97 Electron/37.2.1 Safari/537.36" version="28.0.4" pages="{pages_count}">
{chr(10).join(diagrams)}
</mxfile>'''
    
    # Write the Draw.io file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(drawio_content)
        
        print(f"✓ Generated Draw.io file: {output_file}")
        print(f"✓ Created {pages_count} diagram(s) from Mermaid files")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

def main():
    """Main function with command-line argument parsing"""
    
    parser = argparse.ArgumentParser(
        description="Generate Draw.io files from Mermaid diagrams",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 mermaid_to_drawio.py                              # Process current directory
  python3 mermaid_to_drawio.py /path/to/mermaid/files       # Process specific directory
  python3 mermaid_to_drawio.py input_dir output.drawio      # Specify output file
  python3 mermaid_to_drawio.py -f file1.mmd file2.mmd      # Process specific files
        """
    )
    
    parser.add_argument(
        'input_path',
        nargs='?',
        default='.',
        help='Input directory containing Mermaid files or output file name (default: current directory)'
    )
    
    parser.add_argument(
        'output_file',
        nargs='?',
        default=None,
        help='Output Draw.io file (default: mermaid_diagrams.drawio)'
    )
    
    parser.add_argument(
        '-f', '--files',
        nargs='+',
        metavar='FILE',
        help='Process specific Mermaid files instead of directory'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Determine input files
    if args.files:
        mermaid_files = args.files
        output_file = args.output_file or 'mermaid_diagrams.drawio'
    else:
        input_dir = args.input_path
        
        # Check if input_path is actually the output file
        if args.output_file is None and input_dir.endswith('.drawio'):
            output_file = input_dir
            input_dir = '.'
        else:
            output_file = args.output_file or 'mermaid_diagrams.drawio'
        
        # Find all Mermaid files in the directory
        if not os.path.isdir(input_dir):
            print(f"Error: {input_dir} is not a directory")
            sys.exit(1)
        
        mermaid_files = glob.glob(os.path.join(input_dir, "*.mmd"))
        
        if not mermaid_files:
            print(f"No Mermaid files found in {input_dir}")
            sys.exit(1)
    
    # Sort files for consistent output
    mermaid_files.sort()
    
    if args.verbose:
        print(f"Found {len(mermaid_files)} Mermaid file(s)")
    
    # Generate the Draw.io file
    generate_drawio_file(mermaid_files, output_file, args.verbose)


def convert_mermaid_to_drawio(mermaid_content: str) -> str:
    """
    Convert a single Mermaid diagram to Draw.io XML format.
    
    Args:
        mermaid_content: The Mermaid diagram content
        
    Returns:
        XML string in Draw.io format
    """
    # Create a temporary file to use with generate_drawio_file
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as temp_file:
        temp_file.write(mermaid_content)
        temp_file_path = temp_file.name
    
    try:
        with tempfile.NamedTemporaryFile(mode='r', suffix='.drawio', delete=False) as output_file:
            output_file_path = output_file.name
        
        # Generate the drawio file
        generate_drawio_file([temp_file_path], output_file_path, verbose=False)
        
        # Read the generated content
        if os.path.exists(output_file_path):
            with open(output_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Add XML declaration if not present
            if not content.startswith('<?xml'):
                content = '<?xml version="1.0" encoding="UTF-8"?>\n' + content
            return content
        else:
            # Return minimal valid XML if file generation failed
            return '<?xml version="1.0" encoding="UTF-8"?>\n<mxfile><diagram></diagram></mxfile>'
    
    finally:
        # Clean up temporary files
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        if os.path.exists(output_file_path):
            os.unlink(output_file_path)


def process_mermaid_files(directory: str) -> List[str]:
    """
    Process all Mermaid files in a directory and create Draw.io files.
    
    Args:
        directory: Directory containing .mmd files
        
    Returns:
        List of processed file paths
    """
    if not os.path.exists(directory) or not os.path.isdir(directory):
        return []
    
    # Find all .mmd files
    mmd_files = glob.glob(os.path.join(directory, "*.mmd"))
    
    if not mmd_files:
        return []
    
    processed_files = []
    
    for mmd_file in mmd_files:
        try:
            # Generate corresponding .drawio file
            base_name = os.path.splitext(os.path.basename(mmd_file))[0]
            drawio_file = os.path.join(directory, f"{base_name}.drawio")
            
            # Generate the drawio file
            generate_drawio_file([mmd_file], drawio_file, verbose=False)
            
            if os.path.exists(drawio_file):
                processed_files.append(mmd_file)
        
        except Exception as e:
            # Skip files that can't be processed
            continue
    
    return processed_files


if __name__ == "__main__":
    main()
