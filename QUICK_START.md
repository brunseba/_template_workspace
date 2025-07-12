# MkDocs Template Quick Start Guide

This guide will help you get started with the MkDocs templates using the provided Taskfile.

## Prerequisites

- **Python 3.8+** installed on your system
- **Task** installed ([Installation Guide](https://taskfile.dev/installation/))
- **Git** (optional, for version control)

## Quick Setup

### 1. Install MkDocs with pipx

```bash
# Install everything needed
task install
```

This will:
- Install pipx if not already installed
- Install MkDocs core using pipx
- Install all common plugins

### 2. Initialize Your Project

Choose one of three templates:

```bash
# Basic template (minimal setup)
task init-basic

# Standard template (recommended)
task init-standard

# Advanced template (full features)
task init-advanced
```

### 3. Start Development Server

```bash
# Serve locally
task serve

# Or serve on all interfaces (accessible from network)
task serve-all
```

Your documentation will be available at `http://localhost:8000`

## Available Templates

### Basic Template (`mkdocs-basic-template.yml`)
- Minimal configuration
- Purple color scheme
- Essential plugins only
- Perfect for simple documentation

### Standard Template (`mkdocs-template.yml`)
- Balanced feature set
- Blue color scheme
- Common plugins included
- Good for most projects

### Advanced Template (`mkdocs-advanced-template.yml`)
- Full feature set
- All plugins from analysis
- Advanced navigation with emojis
- Enterprise-ready features

## Common Tasks

### Development

```bash
# Serve documentation locally
task serve

# Build documentation
task build

# Build with strict mode (warnings as errors)
task build-strict

# Validate configuration and build
task validate
```

### Content Management

```bash
# Create a new page
task new-page -- getting-started/installation

# Run basic linting
task lint
```

### Cleanup

```bash
# Clean build artifacts
task clean

# Clean all caches and generated files
task clean-all
```

### Deployment

```bash
# Deploy to GitHub Pages
task deploy-gh-pages

# Force deploy (use with caution)
task deploy-gh-pages-force
```

### Maintenance

```bash
# Show environment info
task info

# List installed plugins
task list-plugins

# Update MkDocs and plugins
task update
```

## Directory Structure

After initialization, your project will have:

```
your-project/
├── mkdocs.yml              # Main configuration file
├── docs/                   # Documentation source
│   └── index.md           # Homepage
├── site/                   # Generated site (ignored in git)
├── Taskfile.yml           # Task automation
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore patterns
└── README.md             # Project documentation
```

## Customization

### 1. Update Configuration

Edit `mkdocs.yml` to customize:
- Site name and description
- Repository URLs
- Navigation structure
- Theme colors
- Plugin settings

### 2. Add Content

Create markdown files in the `docs/` directory:

```bash
# Create a new page
task new-page -- user-guide/getting-started

# Edit the file
vim docs/user-guide/getting-started.md
```

### 3. Update Navigation

Edit the `nav:` section in `mkdocs.yml`:

```yaml
nav:
  - Home: index.md
  - User Guide:
    - Getting Started: user-guide/getting-started.md
    - Advanced Usage: user-guide/advanced-usage.md
  - API Reference: api-reference.md
```

## Plugin Configuration

### Essential Plugins (included in all templates)

- **search**: Full-text search functionality
- **material**: Material Design theme

### Common Plugins (standard/advanced templates)

- **git-revision-date-localized**: Show last updated dates
- **git-committers**: Show page contributors
- **mermaid2**: Diagram support
- **macros**: Template variables and macros
- **minify**: HTML minification

### Advanced Plugins (advanced template only)

- **awesome-pages**: Automatic navigation
- **redirects**: URL redirects
- **include-markdown**: Include external markdown
- **section-index**: Auto-generate section indexes

## Color Schemes

### Blue Theme (Default)
```yaml
palette:
  - scheme: default
    primary: blue
    accent: light blue
```

### Purple Theme
```yaml
palette:
  - scheme: default
    primary: deep purple
    accent: purple
```

### Indigo Theme
```yaml
palette:
  - scheme: default
    primary: indigo
    accent: indigo
```

## Troubleshooting

### Common Issues

1. **MkDocs not found**
   ```bash
   # Ensure pipx is in PATH
   pipx ensurepath
   # Restart shell
   source ~/.zshrc
   ```

2. **Plugin not found**
   ```bash
   # Install missing plugin
   pipx inject mkdocs plugin-name
   ```

3. **Build fails**
   ```bash
   # Check configuration
   task check-config
   # Build with verbose output
   mkdocs build --verbose
   ```

### Getting Help

```bash
# Show all available tasks
task help

# Show environment information
task info

# List installed plugins
task list-plugins
```

## Best Practices

### 1. Version Control

Initialize git repository:
```bash
git init
git add .
git commit -m "Initial documentation setup"
```

### 2. Regular Updates

```bash
# Update MkDocs and plugins monthly
task update
```

### 3. Validate Before Deploy

```bash
# Always validate before deployment
task validate
```

### 4. Use Branches

```bash
# Create feature branches for major changes
git checkout -b feature/new-documentation
```

## Dynamic Content with Macros

The template includes powerful macros for dynamic content generation:

### Using Macros in Markdown

```markdown
# Welcome to {{ metadata.project.name }}

{{ version_info() }}

{{ project_info() }}

## Latest Release

{{ release_notes() }}

## Project Statistics

{{ project_stats() }}
```

### Customizing Metadata

Edit `.metadata.yaml` to customize your project information:

```yaml
project:
  name: "Your Project Name"
  description: "Your project description"
  repository: "https://github.com/yourusername/your-project"
  documentation: "https://yourusername.github.io/your-project/"

release:
  major_features:
    - "Your amazing feature"
    - "Another great feature"
  improvements:
    - "Performance improvements"
    - "Better documentation"

metrics:
  total_documents: 15
  total_pages: 35
  documentation_lines: 5000
```

### Available Macros

- `{{ get_git_tag() }}` - Current git tag
- `{{ get_commit_hash() }}` - Current commit hash
- `{{ version_info() }}` - Version information block
- `{{ project_stats() }}` - Project statistics
- `{{ release_notes() }}` - Release notes
- `{{ build_info() }}` - Build information table
- `{{ contributors() }}` - Contributors list

## Next Steps

1. **Customize** your `mkdocs.yml` configuration
2. **Update** `.metadata.yaml` with your project information
3. **Add** your content to the `docs/` directory
4. **Use macros** for dynamic content generation
5. **Test** locally with `task serve`
6. **Deploy** to GitHub Pages with `task deploy-gh-pages`
7. **Maintain** with regular updates using `task update`

## GitHub Integration

When you're ready to use a real GitHub repository:

1. **Read the GitHub setup guide**: `GITHUB_SETUP.md`
2. **Install GitHub plugins**: `task install-git-plugins`
3. **Configure authentication**: Set up GitHub token
4. **Enable git plugins**: Uncomment in your `mkdocs.yml`

## Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material Theme Documentation](https://squidfunk.github.io/mkdocs-material/)
- [Task Documentation](https://taskfile.dev/)
- [pipx Documentation](https://pypa.github.io/pipx/)
- [GitHub Setup Guide](GITHUB_SETUP.md)

Happy documenting! 📚
