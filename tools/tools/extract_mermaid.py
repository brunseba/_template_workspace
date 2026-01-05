#!/usr/bin/env python3
"""
Extract Mermaid diagrams from markdown files and generate individual .mmd files.
"""

import re
import click
from pathlib import Path
from typing import List, Tuple
import os
import glob
import base64
import xml.etree.ElementTree as ET
import json
import urllib.parse
from .mermaid_to_drawio import generate_drawio_file


def extract_mermaid_blocks(content: str) -> List[Tuple[str, str]]:
    """
    Extract Mermaid code blocks from markdown content.
    
    Returns:
        List of tuples containing (diagram_type, diagram_content)
    """
    # Pattern to match mermaid code blocks (case-insensitive, with optional spaces)
    pattern = r'```\s*mermaid\s*\n(.*?)\n?```'
    matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
    
    diagrams = []
    for match in matches:
        # Extract the diagram type from the first line
        lines = match.strip().split('\n')
        if lines:
            diagram_type = lines[0].strip()
            diagrams.append((diagram_type, match.strip()))
    
    return diagrams


def extract_mermaid_diagrams(content: str) -> List[str]:
    """
    Extract Mermaid diagrams from markdown content (simplified version).
    
    Returns:
        List of diagram content strings
    """
    diagrams = extract_mermaid_blocks(content)
    return [diagram[1] for diagram in diagrams]


def generate_mmd_files(md_file: Path, output_dir: Path, verbose: bool = False) -> int:
    """
    Extract Mermaid diagrams from a markdown file and generate .mmd files.
    
    Args:
        md_file: Path to the input markdown file
        output_dir: Directory to save the generated .mmd files
        verbose: Enable verbose output
    
    Returns:
        Number of diagrams extracted
    """
    # Read the markdown file
    try:
        content = md_file.read_text(encoding='utf-8')
        if verbose:
            click.echo(f"Reading file: {md_file}")
    except Exception as e:
        click.echo(f"Error reading {md_file}: {e}", err=True)
        raise click.ClickException(f"Failed to read input file: {e}")
    
    # Extract Mermaid diagrams
    diagrams = extract_mermaid_blocks(content)
    
    if not diagrams:
        click.echo(f"No Mermaid diagrams found in {md_file}")
        return 0
    
    # Create output directory if it doesn't exist
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        if verbose:
            click.echo(f"Created output directory: {output_dir}")
    except Exception as e:
        click.echo(f"Error creating output directory {output_dir}: {e}", err=True)
        raise click.ClickException(f"Failed to create output directory: {e}")
    
    # Generate .mmd files
    base_name = md_file.stem
    type_count = {}
    generated_count = 0
    
    for diagram_type, diagram_content in diagrams:
        # Handle duplicate diagram types by adding a counter
        if diagram_type in type_count:
            type_count[diagram_type] += 1
            counter = type_count[diagram_type]
            filename = f"{base_name}_{diagram_type}_{counter}.mmd"
        else:
            type_count[diagram_type] = 1
            filename = f"{base_name}_{diagram_type}.mmd"
        
        # Clean filename (remove special characters)
        filename = re.sub(r'[^\w\-_\.]', '_', filename)
        
        output_file = output_dir / filename
        
        try:
            output_file.write_text(diagram_content, encoding='utf-8')
            click.echo(f"Generated: {output_file}", color=True)
            generated_count += 1
        except Exception as e:
            click.echo(f"Error writing {output_file}: {e}", err=True)
    
    return generated_count


def create_drawio_xml(mmd_files: List[Path], output_file: Path) -> None:
    """
    Create a drawio XML file from a list of .mmd files.
    
    Args:
        mmd_files: List of .mmd file paths
        output_file: Path to output .drawio file
    """
    # Create root mxfile element
    mxfile = ET.Element("mxfile")
    mxfile.set("host", "Electron")
    mxfile.set("agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) draw.io/28.0.4 Chrome/138.0.7204.97 Electron/37.2.1 Safari/537.36")
    mxfile.set("version", "28.0.4")
    mxfile.set("pages", str(len(mmd_files)))
    
    for i, mmd_file in enumerate(mmd_files):
        try:
            # Read the mermaid content
            mermaid_content = mmd_file.read_text(encoding='utf-8')
            diagram_name = mmd_file.stem.replace('_', ' ').title()
            
            # Create diagram element
            diagram = ET.SubElement(mxfile, "diagram")
            diagram.set("name", diagram_name)
            diagram.set("id", f"diagram-{i}")
            
            # Create mxGraphModel
            graph_model = ET.SubElement(diagram, "mxGraphModel")
            graph_model.set("dx", "706")
            graph_model.set("dy", "604")
            graph_model.set("grid", "1")
            graph_model.set("gridSize", "10")
            graph_model.set("guides", "1")
            graph_model.set("tooltips", "1")
            graph_model.set("connect", "1")
            graph_model.set("arrows", "1")
            graph_model.set("fold", "1")
            graph_model.set("page", "1")
            graph_model.set("pageScale", "1")
            graph_model.set("pageWidth", "827")
            graph_model.set("pageHeight", "1169")
            graph_model.set("math", "0")
            graph_model.set("shadow", "0")
            
            # Create root element
            root = ET.SubElement(graph_model, "root")
            
            # Create default cells
            cell0 = ET.SubElement(root, "mxCell")
            cell0.set("id", "0")
            
            cell1 = ET.SubElement(root, "mxCell")
            cell1.set("id", "1")
            cell1.set("parent", "0")
            
            # Create UserObject with mermaid data
            user_object = ET.SubElement(root, "UserObject")
            user_object.set("label", "")
            
            # Create mermaid data JSON
            mermaid_data = {
                "data": mermaid_content
            }
            
            # Encode mermaid data as HTML entities
            mermaid_json = json.dumps(mermaid_data, separators=(',', ':'))
            encoded_data = mermaid_json.replace('"', '&quot;').replace('\n', '\\n').replace('<', '&lt;').replace('>', '&gt;')
            user_object.set("mermaidData", f"{{{encoded_data}}}")
            user_object.set("id", f"mermaid-{i}")
            
            # Create mxCell for the diagram
            mx_cell = ET.SubElement(user_object, "mxCell")
            mx_cell.set("style", "shape=image;noLabel=1;verticalAlign=top;imageAspect=1;image=data:image/svg+xml,")
            mx_cell.set("vertex", "1")
            mx_cell.set("parent", "1")
            
            # Create geometry
            geometry = ET.SubElement(mx_cell, "mxGeometry")
            geometry.set("x", "260")
            geometry.set("y", "130")
            geometry.set("width", "400")
            geometry.set("height", "300")
            geometry.set("as", "geometry")
            
        except Exception as e:
            click.echo(f"Error processing {mmd_file}: {e}", err=True)
            continue
    
    # Write the XML file
    try:
        tree = ET.ElementTree(mxfile)
        ET.indent(tree, space="  ", level=0)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        click.echo(f"Generated drawio file: {output_file}")
    except Exception as e:
        click.echo(f"Error writing drawio file {output_file}: {e}", err=True)


def consolidate_mmd_to_drawio(md_file: Path, output_dir: Path) -> None:
    """
    Consolidate all .mmd files from a markdown file into a single .drawio file.
    
    Args:
        md_file: Path to the source markdown file
        output_dir: Directory containing the .mmd files
    """
    base_name = md_file.stem
    
    # Find all .mmd files that match the source file
    mmd_pattern = f"{base_name}_*.mmd"
    mmd_files = list(output_dir.glob(mmd_pattern))
    
    if not mmd_files:
        click.echo(f"No .mmd files found for {md_file.name}")
        return
    
    # Sort files for consistent ordering
    mmd_files.sort()
    
    # Create output drawio file
    drawio_file = output_dir / f"{base_name}.drawio"
    
    click.echo(f"Consolidating {len(mmd_files)} diagrams from {md_file.name} into {drawio_file.name}")
    create_drawio_xml(mmd_files, drawio_file)


def find_markdown_files(input_path: Path, recursive: bool = False) -> List[Path]:
    """
    Find all markdown files in the given path.

    Args:
        input_path: Path to file or directory to search.
        recursive: If True, search subdirectories recursively.

    Returns:
        List of markdown file paths.
    """
    markdown_files = []
    
    if input_path.is_file():
        if input_path.suffix.lower() in ['.md', '.markdown']:
            markdown_files.append(input_path)
        else:
            click.echo(f"Warning: {input_path} is not a markdown file", err=True)
    elif input_path.is_dir():
        pattern = '**/*.md' if recursive else '*.md'
        markdown_files.extend(input_path.glob(pattern))
        
        # Also search for .markdown files
        pattern = '**/*.markdown' if recursive else '*.markdown'
        markdown_files.extend(input_path.glob(pattern))
    
    return sorted(markdown_files)


@click.command()
@click.argument('input_path', type=click.Path(exists=True, path_type=Path))
@click.option('-o', '--output-dir', default='mermaid_diagrams', type=click.Path(file_okay=False, writable=True, path_type=Path), help='Output directory for .mmd files.')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output.')
@click.option('-r', '--recursive', is_flag=True, help='Process directories recursively.')
@click.option('--dry-run', is_flag=True, help='Show what would be extracted without creating files.')
@click.option('--drawio', is_flag=True, help='Generate .drawio files by consolidating .mmd files per source markdown file.')
@click.option('--advanced-drawio', is_flag=True, help='Generate .drawio files using the advanced XML structure with Mermaid data embedding.')
@click.version_option(version='0.1.0', prog_name='mermaid-extractor')
def main(input_path, output_dir, verbose, recursive, dry_run, drawio, advanced_drawio):
    """
    Extract Mermaid diagrams from MARKDOWN files or directories and generate individual .mmd files.
    
    INPUT_PATH can be a single markdown file or a directory containing markdown files.
    
    Each diagram will be saved as a separate .mmd file with the naming convention:
    {source_filename}_{diagram_type}.mmd
    
    For duplicate diagram types, a counter is added:
    {source_filename}_{diagram_type}_{counter}.mmd
    
    Examples:
    
    \b
    # Extract diagrams from a single markdown file
    mermaid-extractor docs/example.md
    
    \b
    # Extract from all markdown files in a directory
    mermaid-extractor docs/ -o output/
    
    \b
    # Extract recursively from all subdirectories
    mermaid-extractor docs/ -r -o output/
    
    \b
    # Preview what would be extracted
    mermaid-extractor docs/ --dry-run
    
    \b
    # Generate .drawio files with consolidated diagrams
    mermaid-extractor docs/ --drawio -o output/
    
    \b
    # Extract and generate drawio files with verbose output
    mermaid-extractor docs/ -r -v --drawio -o output/
    """
    # Find all markdown files
    markdown_files = find_markdown_files(input_path, recursive)
    
    if not markdown_files:
        click.echo("No markdown files found in the specified path.")
        return
    
    if verbose:
        click.echo(f"Input path: {input_path}")
        click.echo(f"Output directory: {output_dir}")
        click.echo(f"Recursive: {recursive}")
        click.echo(f"Dry run: {dry_run}")
        click.echo(f"Generate drawio: {drawio}")
        click.echo(f"Advanced drawio: {advanced_drawio}")
        click.echo(f"Found {len(markdown_files)} markdown file(s)")
        click.echo("---")
    
    total_diagrams = 0
    processed_files = 0
    files_with_diagrams = []
    
    for file_path in markdown_files:
        try:
            if dry_run:
                count = preview_extraction(file_path, output_dir)
            else:
                count = process_file(file_path, output_dir, verbose, dry_run)
            
            total_diagrams += count
            if count > 0:
                processed_files += 1
                files_with_diagrams.append(file_path)
                
        except Exception as e:
            click.echo(f"Error processing {file_path}: {e}", err=True)
            continue
    
    # Generate drawio files if requested
    if (drawio or advanced_drawio) and not dry_run and files_with_diagrams:
        click.echo("\nGenerating drawio files...")
        for file_path in files_with_diagrams:
            try:
                if advanced_drawio:
                    # Use the advanced Draw.io generation with Mermaid data embedding
                    base_name = file_path.stem
                    mmd_pattern = f"{base_name}_*.mmd"
                    mmd_files = list(output_dir.glob(mmd_pattern))
                    
                    if mmd_files:
                        mmd_files.sort()
                        mmd_file_paths = [str(f) for f in mmd_files]
                        drawio_file = str(output_dir / f"{base_name}_advanced.drawio")
                        generate_drawio_file(mmd_file_paths, drawio_file, verbose)
                else:
                    # Use the original Draw.io generation
                    consolidate_mmd_to_drawio(file_path, output_dir)
            except Exception as e:
                click.echo(f"Error creating drawio file for {file_path}: {e}", err=True)
    
    # Summary
    if dry_run:
        summary = f"\nSummary: Would extract {total_diagrams} diagram(s) from {processed_files} file(s)"
        if drawio or advanced_drawio:
            drawio_type = "advanced " if advanced_drawio else ""
            summary += f" and generate {len(files_with_diagrams)} {drawio_type}drawio file(s)"
        click.echo(summary)
    else:
        summary = f"\nSummary: Extracted {total_diagrams} diagram(s) from {processed_files} file(s) to {output_dir}"
        if (drawio or advanced_drawio) and files_with_diagrams:
            drawio_type = "advanced " if advanced_drawio else ""
            summary += f" and generated {len(files_with_diagrams)} {drawio_type}drawio file(s)"
        click.echo(summary)


def process_file(file_path: Path, output_dir: Path, verbose: bool, dry_run: bool) -> int:
    """
    Process a single markdown file to extract Mermaid diagrams.

    Args:
        file_path: Path to the markdown file to process.
        output_dir: Directory to save the generated .mmd files.
        verbose: Enable verbose output.
        dry_run: If True, only simulate the execution.

    Returns:
        Number of diagrams processed.
    """
    try:
        if verbose:
            click.echo(f"Processing file: {file_path}")
        return generate_mmd_files(file_path, output_dir, verbose=verbose) if not dry_run else preview_extraction(file_path, output_dir)
    except Exception as e:
        click.echo(f"Failed to process file '{file_path}': {e}", err=True)
        return 0


def preview_extraction(file_path: Path, output_dir: Path) -> int:
    """
    Simulate extraction without creating files.

    Args:
        file_path: Path to the markdown file to process.
        output_dir: Directory to which the files would be saved.

    Returns:
        Number of diagrams found.
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        diagrams = extract_mermaid_blocks(content)
        if not diagrams:
            click.echo(f"No Mermaid diagrams found in {file_path}.")
            return 0

        click.echo(f"Found {len(diagrams)} diagram(s) in {file_path}: ")

        base_name = file_path.stem
        type_count = {}
        for diagram_type, _ in diagrams:
            if diagram_type in type_count:
                type_count[diagram_type] += 1
                counter = type_count[diagram_type]
                filename = f"{base_name}_{diagram_type}_{counter}.mmd"
            else:
                type_count[diagram_type] = 1
                filename = f"{base_name}_{diagram_type}.mmd"

            filename = re.sub(r'[^\w\-_\.]', '_', filename)
            click.echo(f"  - {output_dir / filename}")
        return len(diagrams)
    except Exception as e:
        click.echo(f"Error reading file {file_path}: {e}", err=True)
        return 0


if __name__ == "__main__":
    main()
