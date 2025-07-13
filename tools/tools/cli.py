#!/usr/bin/env python3
"""
Unified CLI interface for mermaid-tools
Provides access to both mermaid extraction and Draw.io conversion tools
"""

import click
from .extract_mermaid import main as extract_main
from .mermaid_to_drawio import main as drawio_main


@click.group()
@click.version_option(version='0.3.0', prog_name='mermaid-tools')
@click.pass_context
def cli(ctx):
    """
    Mermaid Tools - Extract and convert Mermaid diagrams
    
    This toolkit provides utilities for:
    - Extracting Mermaid diagrams from markdown files
    - Converting Mermaid diagrams to Draw.io format
    - Direct conversion from markdown to Draw.io format
    
    Use --help with any command for more details.
    """
    ctx.ensure_object(dict)


@cli.command('extract')
@click.argument('input_path', type=click.Path(exists=True))
@click.option('-o', '--output-dir', default='mermaid_diagrams', type=click.Path(file_okay=False, writable=True), help='Output directory for .mmd files.')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output.')
@click.option('-r', '--recursive', is_flag=True, help='Process directories recursively.')
@click.option('--dry-run', is_flag=True, help='Show what would be extracted without creating files.')
@click.option('--drawio', is_flag=True, help='Generate .drawio files by consolidating .mmd files per source markdown file.')
@click.option('--advanced-drawio', is_flag=True, help='Generate .drawio files using the advanced XML structure with Mermaid data embedding.')
def extract_command(input_path, output_dir, verbose, recursive, dry_run, drawio, advanced_drawio):
    """
    Extract Mermaid diagrams from markdown files and generate individual .mmd files.
    
    INPUT_PATH can be a single markdown file or a directory containing markdown files.
    
    Examples:
    
    \b
    # Extract diagrams from a single markdown file
    mermaid-tools extract docs/example.md
    
    \b
    # Extract from all markdown files in a directory
    mermaid-tools extract docs/ -o output/
    
    \b
    # Extract recursively with advanced Draw.io generation
    mermaid-tools extract docs/ -r --advanced-drawio -o output/
    """
    # Convert string paths to Path objects for compatibility
    from pathlib import Path
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    
    # Import and call the original function with converted arguments
    from .extract_mermaid import main as extract_main
    import sys
    
    # Save original sys.argv and replace it temporarily
    original_argv = sys.argv[:]
    
    # Build new argv for the extract_main function
    new_argv = ['mermaid-tools', str(input_path)]
    if output_dir != Path('mermaid_diagrams'):
        new_argv.extend(['-o', str(output_dir)])
    if verbose:
        new_argv.append('-v')
    if recursive:
        new_argv.append('-r')
    if dry_run:
        new_argv.append('--dry-run')
    if drawio:
        new_argv.append('--drawio')
    if advanced_drawio:
        new_argv.append('--advanced-drawio')
    
    sys.argv = new_argv
    
    try:
        extract_main.callback(input_path, output_dir, verbose, recursive, dry_run, drawio, advanced_drawio)
    finally:
        sys.argv = original_argv


@cli.command('to-drawio')
@click.argument('input_path', default='.')
@click.argument('output_file', required=False)
@click.option('-f', '--files', multiple=True, help='Process specific Mermaid files instead of directory.')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output.')
def drawio_command(input_path, output_file, files, verbose):
    """
    Generate Draw.io files from Mermaid diagrams.
    
    INPUT_PATH is the directory containing .mmd files (default: current directory).
    OUTPUT_FILE is the name of the output .drawio file (default: mermaid_diagrams.drawio).
    
    Examples:
    
    \b
    # Convert all .mmd files in current directory
    mermaid-tools to-drawio
    
    \b
    # Convert .mmd files from specific directory
    mermaid-tools to-drawio mermaid_diagrams/
    
    \b
    # Convert specific files
    mermaid-tools to-drawio -f diagram1.mmd -f diagram2.mmd
    
    \b
    # Specify output file
    mermaid-tools to-drawio input_dir/ my_diagrams.drawio
    """
    # Import and call the drawio function
    from .mermaid_to_drawio import generate_drawio_file
    import os
    import glob
    
    if files:
        # Process specific files
        mermaid_files = list(files)
        output = output_file or 'mermaid_diagrams.drawio'
    else:
        # Process directory
        input_dir = input_path
        
        # Check if input_path is actually the output file
        if output_file is None and input_dir.endswith('.drawio'):
            output = input_dir
            input_dir = '.'
        else:
            output = output_file or 'mermaid_diagrams.drawio'
        
        # Find all Mermaid files in the directory
        if not os.path.isdir(input_dir):
            click.echo(f"Error: {input_dir} is not a directory")
            return
        
        mermaid_files = glob.glob(os.path.join(input_dir, "*.mmd"))
        
        if not mermaid_files:
            click.echo(f"No Mermaid files found in {input_dir}")
            return
    
    # Sort files for consistent output
    mermaid_files.sort()
    
    if verbose:
        click.echo(f"Found {len(mermaid_files)} Mermaid file(s)")
    
    # Generate the Draw.io file
    generate_drawio_file(mermaid_files, output, verbose)


@cli.command('md-to-drawio')
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_file', required=False)
@click.option('-r', '--recursive', is_flag=True, help='Process directories recursively.')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output.')
@click.option('--temp-dir', default='temp_mermaid', type=click.Path(file_okay=False), help='Temporary directory for intermediate .mmd files.')
@click.option('--keep-temp', is_flag=True, help='Keep temporary .mmd files after conversion.')
@click.option('--separate-files', is_flag=True, help='Create separate .drawio files for each markdown file.')
def md_to_drawio_command(input_path, output_file, recursive, verbose, temp_dir, keep_temp, separate_files):
    """
    Convert Mermaid diagrams from markdown files directly to Draw.io format.
    
    This command combines extraction and conversion in a single step.
    
    INPUT_PATH can be a single markdown file or a directory containing markdown files.
    OUTPUT_FILE is the name of the output .drawio file (default: diagrams.drawio).
    
    Examples:
    
    \b
    # Convert a single markdown file
    mermaid-tools md-to-drawio docs/example.md
    
    \b
    # Convert all markdown files in a directory
    mermaid-tools md-to-drawio docs/ output.drawio
    
    \b
    # Convert recursively with separate files for each markdown
    mermaid-tools md-to-drawio docs/ -r --separate-files
    
    \b
    # Convert with verbose output and keep temporary files
    mermaid-tools md-to-drawio docs/ -v --keep-temp
    """
    import os
    import tempfile
    import shutil
    from pathlib import Path
    from .extract_mermaid import extract_mermaid_blocks, find_markdown_files
    from .mermaid_to_drawio import generate_drawio_file
    
    input_path = Path(input_path)
    temp_dir = Path(temp_dir)
    
    # Find all markdown files
    markdown_files = find_markdown_files(input_path, recursive)
    
    if not markdown_files:
        click.echo("No markdown files found in the specified path.")
        return
    
    if verbose:
        click.echo(f"Found {len(markdown_files)} markdown file(s)")
    
    # Create temporary directory for .mmd files
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        if separate_files:
            # Create separate .drawio files for each markdown file
            for md_file in markdown_files:
                if verbose:
                    click.echo(f"Processing {md_file}...")
                
                # Extract diagrams from this markdown file
                content = md_file.read_text(encoding='utf-8')
                diagrams = extract_mermaid_blocks(content)
                
                if not diagrams:
                    if verbose:
                        click.echo(f"  No diagrams found in {md_file}")
                    continue
                
                # Create temporary .mmd files for this markdown file
                temp_mmd_files = []
                base_name = md_file.stem
                type_count = {}
                
                for diagram_type, diagram_content in diagrams:
                    if diagram_type in type_count:
                        type_count[diagram_type] += 1
                        counter = type_count[diagram_type]
                        filename = f"{base_name}_{diagram_type}_{counter}.mmd"
                    else:
                        type_count[diagram_type] = 1
                        filename = f"{base_name}_{diagram_type}.mmd"
                    
                    # Clean filename
                    import re
                    filename = re.sub(r'[^\w\-_\.]', '_', filename)
                    
                    temp_mmd_file = temp_dir / filename
                    temp_mmd_file.write_text(diagram_content, encoding='utf-8')
                    temp_mmd_files.append(str(temp_mmd_file))
                
                # Generate .drawio file for this markdown file
                drawio_output = f"{base_name}.drawio" if not output_file else output_file
                if len(markdown_files) > 1 and not output_file:
                    # Add index to avoid overwriting
                    drawio_output = f"{base_name}_diagrams.drawio"
                
                generate_drawio_file(temp_mmd_files, drawio_output, verbose)
                
                if verbose:
                    click.echo(f"  Generated {drawio_output} with {len(temp_mmd_files)} diagram(s)")
        
        else:
            # Create single .drawio file with all diagrams
            all_mmd_files = []
            total_diagrams = 0
            
            for md_file in markdown_files:
                if verbose:
                    click.echo(f"Processing {md_file}...")
                
                # Extract diagrams from this markdown file
                content = md_file.read_text(encoding='utf-8')
                diagrams = extract_mermaid_blocks(content)
                
                if not diagrams:
                    if verbose:
                        click.echo(f"  No diagrams found in {md_file}")
                    continue
                
                # Create temporary .mmd files
                base_name = md_file.stem
                type_count = {}
                
                for diagram_type, diagram_content in diagrams:
                    if diagram_type in type_count:
                        type_count[diagram_type] += 1
                        counter = type_count[diagram_type]
                        filename = f"{base_name}_{diagram_type}_{counter}.mmd"
                    else:
                        type_count[diagram_type] = 1
                        filename = f"{base_name}_{diagram_type}.mmd"
                    
                    # Clean filename
                    import re
                    filename = re.sub(r'[^\w\-_\.]', '_', filename)
                    
                    temp_mmd_file = temp_dir / filename
                    temp_mmd_file.write_text(diagram_content, encoding='utf-8')
                    all_mmd_files.append(str(temp_mmd_file))
                    total_diagrams += 1
                
                if verbose:
                    click.echo(f"  Extracted {len(diagrams)} diagram(s)")
            
            if all_mmd_files:
                # Generate single .drawio file with all diagrams
                drawio_output = output_file or 'diagrams.drawio'
                generate_drawio_file(all_mmd_files, drawio_output, verbose)
                
                click.echo(f"\nGenerated {drawio_output} with {total_diagrams} diagram(s) from {len(markdown_files)} markdown file(s)")
            else:
                click.echo("No Mermaid diagrams found in any markdown files.")
    
    finally:
        # Clean up temporary files unless --keep-temp is specified
        if not keep_temp:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
                if verbose:
                    click.echo(f"Cleaned up temporary directory: {temp_dir}")
        else:
            if verbose:
                click.echo(f"Temporary files kept in: {temp_dir}")


@cli.command('version')
def version():
    """Show version information."""
    click.echo("mermaid-tools version 0.3.0")
    click.echo("Extract and convert Mermaid diagrams")


if __name__ == '__main__':
    cli()
