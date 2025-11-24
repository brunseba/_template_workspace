#!/usr/bin/env python3
"""
MkDocs Exports Docs - Federated CLI for documentation export and project management.
"""

import click
import sys


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """MkDocs documentation export and project management scripts."""
    pass


@cli.command(name="export-workload")
@click.option(
    "--input",
    "-i",
    default="../docs/project-plan/weekly-charge-breakdown.md",
    help="Input markdown file path",
)
@click.option(
    "--output",
    "-o",
    default="../docs/export/RH_OVE_Weekly_Workload_Breakdown.xlsx",
    help="Output XLSX file path",
)
def export_workload_cmd(input, output):
    """Export weekly workload breakdown to multi-sheet XLSX file."""
    from .export_workload_to_xlsx import parse_markdown_tables, create_xlsx_workbook

    click.echo(f"Parsing workload data from {input}...")
    data = parse_markdown_tables(input)

    click.echo(f"Creating XLSX workbook with multiple sheets...")
    create_xlsx_workbook(data, output)

    click.echo(f"\n✅ Export complete! Multi-sheet XLSX file created: {output}")
    click.echo(f"📄 Sheets included:")
    for sheet_name in data.keys():
        click.echo(f"  - {sheet_name}")


@cli.command(name="convert-docs")
def convert_docs_cmd():
    """Convert MkDocs documentation to comprehensive DOCX file using Pandoc."""
    from .convert_docs_to_docx import main as convert_main

    sys.exit(convert_main())


@cli.command(name="convert-by-chapter")
def convert_by_chapter_cmd():
    """Convert MkDocs documentation to separate DOCX files by chapter."""
    from .convert_docs_to_docx_by_chapter import main as convert_chapter_main

    convert_chapter_main()


@cli.command(name="convert-with-filter")
def convert_with_filter_cmd():
    """Convert MkDocs documentation to DOCX using pandoc-mermaid-filter."""
    from .convert_docs_to_docx_with_filter import main as convert_filter_main

    convert_filter_main()


@cli.command(name="howto")
def howto_cmd():
    """Display usage examples and how-to guide."""
    from . import __version__
    
    click.echo("\n" + "=" * 70)
    click.echo("  MkDocs Export Tools - How To Guide")
    click.echo("  Version: " + __version__)
    click.echo("=" * 70 + "\n")
    
    click.echo("📋 AVAILABLE COMMANDS:\n")
    
    click.echo("1. Export Workload to XLSX")
    click.echo("   Export weekly workload breakdown to Excel spreadsheet")
    click.echo("   ")
    click.secho("   $ mkdocs-exports-docs export-workload", fg="green")
    click.echo("   $ mkdocs-exports-docs export-workload -i docs/plan.md -o output.xlsx\n")
    
    click.echo("2. Convert Full Documentation to DOCX")
    click.echo("   Convert all MkDocs documentation to a single DOCX file")
    click.echo("   ")
    click.secho("   $ mkdocs-exports-docs convert-docs", fg="green")
    click.echo("   ")
    click.echo("   Requirements: pandoc, docker/npx for Mermaid diagrams\n")
    
    click.echo("3. Convert Documentation by Chapter")
    click.echo("   Create separate DOCX files for each chapter")
    click.echo("   ")
    click.secho("   $ mkdocs-exports-docs convert-by-chapter", fg="green")
    click.echo("   ")
    click.echo("   Requirements: pandoc, mermaid-filter\n")
    
    click.echo("4. Convert with Mermaid Filter")
    click.echo("   Convert documentation using pandoc-mermaid-filter")
    click.echo("   ")
    click.secho("   $ mkdocs-exports-docs convert-with-filter", fg="green")
    click.echo("   ")
    click.echo("   Requirements: pandoc, mermaid-filter\n")
    
    click.echo("📦 INSTALLATION:\n")
    click.echo("   Using pipx (recommended):")
    click.secho("   $ pipx install .", fg="cyan")
    click.echo("   ")
    click.echo("   Using uv:")
    click.secho("   $ uv run mkdocs-exports-docs <command>", fg="cyan")
    click.echo("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    cli()
