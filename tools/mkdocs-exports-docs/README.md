# RH OVE Scripts

This directory contains Python scripts for managing and exporting RH OVE project data.

## Setup

This project uses `uv` for dependency management. To set up the environment:

```bash
cd scripts
uv sync
```

## Scripts

### export_workload_to_xlsx.py

Exports the weekly workload breakdown from the markdown documentation to a multi-sheet XLSX file.

**Usage:**
```bash
# From the scripts directory
uv run python export_workload_to_xlsx.py

# Or using the installed script command
uv run export-workload
```

**Output:**
- Creates `../docs/export/RH_OVE_Weekly_Workload_Breakdown.xlsx`
- Contains multiple sheets with workload data organized by project and persona

## Dependencies

- `openpyxl>=3.1.5` - For Excel file creation and manipulation

## Task Runner

This project uses Go's `task` as a task runner. To see available tasks:

```bash
task --list
```

### Common Tasks

```bash
# Setup environment
task setup

# Export workload data
task export-workload

# Check code syntax
task check

# Clean cache files
task clean

# Update dependencies
task update

# Show project info
task info

# Watch for changes
task watch
```

## Development

To add new dependencies:
```bash
task add <package-name>
# or directly:
uv add <package-name>
```

To set up development tools:
```bash
task dev-setup
```

To run the development workflow:
```bash
task dev
```

To build and validate:
```bash
task build
```
