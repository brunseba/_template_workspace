# Mermaid Tools

A comprehensive toolkit for extracting Mermaid diagrams from markdown files and converting them to various formats including Draw.io.

## Features

- **Extract Mermaid diagrams** from markdown code blocks
- **Generate individual .mmd files** for each diagram
- **Convert Mermaid diagrams to Draw.io format** with embedded Mermaid data
- **Unified CLI interface** for easy access to all tools
- **Support for multiple diagram types** in a single markdown file
- **Recursive directory processing**
- **Advanced Draw.io generation** with proper XML structure
- **Dry-run mode** for previewing extractions

## Installation

```bash
uv pip install -e .
```

## Usage

### Unified CLI Interface

The main interface provides access to all tools:

```bash
mermaid-tools --help
```

#### Extract Mermaid Diagrams

```bash
# Extract from a single markdown file
mermaid-tools extract docs/example.md

# Extract from all markdown files in a directory
mermaid-tools extract docs/ -o output/

# Extract recursively with advanced Draw.io generation
mermaid-tools extract docs/ -r --advanced-drawio -o output/
```

#### Convert to Draw.io

```bash
# Convert all .mmd files in current directory
mermaid-tools to-drawio

# Convert .mmd files from specific directory
mermaid-tools to-drawio mermaid_diagrams/

# Convert specific files
mermaid-tools to-drawio -f diagram1.mmd -f diagram2.mmd
```

### Individual Tools

You can also use the tools individually:

#### Mermaid Extractor

```bash
mermaid-extractor docs/example.md
```

**Options:**
- `-o, --output-dir`: Output directory for .mmd files (default: `mermaid_diagrams`)
- `-v, --verbose`: Enable verbose output
- `-r, --recursive`: Process directories recursively
- `--dry-run`: Show what would be extracted without creating files
- `--drawio`: Generate .drawio files by consolidating .mmd files per source markdown file
- `--advanced-drawio`: Generate .drawio files using advanced XML structure with Mermaid data embedding

#### Mermaid to Draw.io Converter

```bash
mermaid-to-drawio input_directory/ output.drawio
```

**Options:**
- `-f, --files`: Process specific Mermaid files instead of directory
- `-v, --verbose`: Enable verbose output

## Examples

### Extract and Convert Workflow

```bash
# 1. Extract diagrams from markdown files
mermaid-tools extract docs/ -o diagrams/ -v

# 2. Convert extracted diagrams to Draw.io
mermaid-tools to-drawio diagrams/ my_diagrams.drawio -v
```

### Advanced Draw.io Generation

```bash
# Extract with advanced Draw.io generation (embedded Mermaid data)
mermaid-tools extract docs/ --advanced-drawio -o output/
```

### Dry Run and Preview

```bash
# Preview what would be extracted
mermaid-tools extract docs/ --dry-run
```

## Output Files

### .mmd Files

The tool generates .mmd files with the naming convention:
- `{source_filename}_{diagram_type}.mmd`
- For duplicates: `{source_filename}_{diagram_type}_{counter}.mmd`

Example outputs:
- `example_flowchart.mmd`
- `example_classDiagram.mmd`
- `example_sequenceDiagram_2.mmd` (if multiple sequence diagrams exist)

### .drawio Files

**Standard Draw.io files:** Compatible with Draw.io application for viewing and editing.

**Advanced Draw.io files:** Include embedded Mermaid data in the XML structure, allowing for better integration and future processing.

## Supported Diagram Types

The tools support all Mermaid diagram types:
- Flowcharts
- Sequence diagrams
- Class diagrams
- State diagrams
- Entity relationship diagrams
- User journey diagrams
- Gantt charts
- Pie charts
- Git graphs
- And more...

## Development

### Project Structure

```
tools/
├── tools/
│   ├── __init__.py
│   ├── cli.py              # Unified CLI interface
│   ├── extract_mermaid.py  # Mermaid extraction tool
│   └── mermaid_to_drawio.py # Draw.io conversion tool
├── pyproject.toml
└── README.md
```

### Running Tests

```bash
uv run pytest
```

### Code Formatting

```bash
uv run black tools/
uv run flake8 tools/
```

