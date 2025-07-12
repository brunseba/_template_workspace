# MkDocs Template Documentation

This directory contains a comprehensive MkDocs template based on the analysis of 8 existing mkdocs.yml files found in the Personnel and Professionel directories.

## Analysis Summary

The following mkdocs.yml files were analyzed:

### Professional Projects
1. **Platform Engineering (PE)** - `/Professionel/pe/mkdocs.yml`
2. **IA Lab for Dev** - `/Professionel/ia-lab-for-dev/mkdocs.yml`
3. **NetApp ActiveIQ** - `/Professionel/donnees-d-entree/PE-AsProduct/netapp/mkdocs.yml`

### Personal Projects
1. **Temporal.io Tech Watch** - `/Personnel/temporal-io-tech-watch/mkdocs.yml`
2. **Deezer CLI** - `/Personnel/deezer/mkdocs.yml`
3. **Private DNS Zone** - `/Personnel/private-dns-zone/mkdocs.yml`
4. **Messaging System Tech Watch** - `/Personnel/messaging-system-tech-watch/mkdocs.yml`
5. **K8s Tools** - `/Personnel/k8s-tools/mkdocs.yml`

## Common Patterns Identified

### 1. Theme Configuration
- **Material Theme**: All projects use the Material theme for MkDocs
- **Color Schemes**: 
  - Blue (most common): 5 projects
  - Deep Purple: 2 projects
  - Indigo: 1 project
- **Dark/Light Mode**: All projects implement theme switching
- **Typography**: Roboto font family is consistently used

### 2. Navigation Features
Common navigation features across projects:
- `navigation.tabs` - Used in 7/8 projects
- `navigation.sections` - Used in 7/8 projects
- `navigation.expand` - Used in 7/8 projects
- `navigation.top` - Used in 7/8 projects
- `navigation.path` - Used in 5/8 projects
- `search.highlight` - Used in 8/8 projects
- `content.code.copy` - Used in 8/8 projects

### 3. Markdown Extensions
Most frequently used extensions:
- `admonition` - Used in 7/8 projects
- `pymdownx.details` - Used in 7/8 projects
- `pymdownx.superfences` - Used in 8/8 projects (with Mermaid support)
- `pymdownx.tabbed` - Used in 7/8 projects
- `pymdownx.highlight` - Used in 8/8 projects
- `pymdownx.emoji` - Used in 6/8 projects
- `pymdownx.tasklist` - Used in 6/8 projects

### 4. Plugins
Common plugins used:
- `search` - Used in 8/8 projects
- `git-revision-date-localized` - Used in 5/8 projects
- `git-committers` - Used in 3/8 projects
- `mermaid2` - Used in 3/8 projects

### 5. Repository Configuration
Standard repository setup includes:
- `repo_name` - GitHub repository name
- `repo_url` - GitHub repository URL
- `edit_uri` - Edit path for GitHub integration
- `copyright` - Copyright notice

## Template Features

The `mkdocs-template.yml` file includes:

### Core Configuration
- Site metadata (name, description, author, URL)
- Repository integration
- Copyright information

### Theme Setup
- Material theme with blue color scheme
- Dark/light mode toggle
- Responsive design features
- Code highlighting and copying

### Plugin Configuration
- Search functionality
- Git revision date tracking
- Future extensibility for additional plugins

### Markdown Extensions
- Admonitions for callouts
- Code highlighting with syntax support
- Mermaid diagram support
- Tabbed content
- Task lists
- Emoji support

### Navigation Structure
- Hierarchical navigation
- Logical grouping of content
- Extensible structure

## Customization Guide

### 1. Basic Setup
Replace the following placeholders in `mkdocs-template.yml`:

```yaml
site_name: Your Project Name
site_description: Your project description
site_author: Your Name
site_url: https://yourusername.github.io/your-project
repo_name: yourusername/your-project
repo_url: https://github.com/yourusername/your-project
```

### 2. Color Scheme Options
Based on the analysis, popular color schemes include:

**Blue Theme (Recommended)**
```yaml
palette:
  - scheme: default
    primary: blue
    accent: light blue
```

**Deep Purple Theme**
```yaml
palette:
  - scheme: default
    primary: deep purple
    accent: purple
```

**Indigo Theme**
```yaml
palette:
  - scheme: default
    primary: indigo
    accent: indigo
```

### 3. Advanced Plugin Configuration

For projects needing advanced features, consider adding:

```yaml
plugins:
  - search:
      lang: en
  - git-revision-date-localized:
      enable_creation_date: true
      type: timeago
      timezone: UTC
  - git-committers:
      repository: yourusername/your-project
      branch: main
  - mermaid2:
      version: '11.4.0'
```

### 4. Navigation Customization

Adapt the navigation structure to your project needs:

```yaml
nav:
  - Home: index.md
  - Getting Started:
    - Overview: getting-started/overview.md
    - Installation: getting-started/installation.md
  - User Guide:
    - Basic Usage: user-guide/basic-usage.md
    - Advanced Usage: user-guide/advanced-usage.md
  - API Reference:
    - Endpoints: api-reference/endpoints.md
    - Data Models: api-reference/data-models.md
  - Development:
    - Contributing: development/contributing.md
    - Testing: development/testing.md
```

## Best Practices

Based on the analysis of existing projects:

### 1. Content Organization
- Use hierarchical navigation for complex projects
- Group related content together
- Maintain consistent naming conventions

### 2. Feature Selection
- Always include search functionality
- Use code copying for technical documentation
- Enable dark/light mode toggle
- Include git revision dates for maintenance

### 3. Styling
- Stick to Material Design principles
- Use consistent color schemes
- Implement responsive navigation
- Enable syntax highlighting for code blocks

### 4. Documentation Structure
Common documentation patterns:
- **Getting Started**: Overview, installation, quick start
- **User Guide**: Basic and advanced usage
- **API Reference**: Endpoints, data models
- **Development**: Contributing, testing, architecture

## Advanced Configurations

### 1. Custom CSS and JavaScript
```yaml
extra_css:
  - stylesheets/extra.css
extra_javascript:
  - javascripts/extra.js
```

### 2. Social Links
```yaml
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/yourusername/project
    - icon: fontawesome/solid/envelope
      link: mailto:your-email@example.com
```

### 3. Analytics Integration
```yaml
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

## Migration Guide

To migrate from an existing MkDocs configuration:

1. **Backup your current mkdocs.yml**
2. **Copy the template** to your project
3. **Update placeholders** with your project details
4. **Migrate your navigation** structure
5. **Test the build** locally with `mkdocs serve`
6. **Deploy** when satisfied

## Troubleshooting

### Common Issues

1. **Plugin not found**: Ensure plugins are installed with `pip install mkdocs-plugin-name`
2. **Theme not loading**: Verify Material theme is installed with `pip install mkdocs-material`
3. **Navigation not working**: Check YAML indentation and file paths
4. **Mermaid diagrams not rendering**: Ensure mermaid2 plugin is installed

### Dependencies

Core dependencies for the template:
```bash
pip install mkdocs
pip install mkdocs-material
pip install mkdocs-git-revision-date-localized-plugin
pip install mkdocs-git-committers-plugin
pip install mkdocs-mermaid2-plugin
```

## Macros and Dynamic Content

The template includes `macros.py` which provides dynamic content generation:

### Available Macros

- **`{{ get_git_tag() }}`** - Gets the latest git tag
- **`{{ get_commit_hash() }}`** - Gets current commit hash (short)
- **`{{ get_branch_name() }}`** - Gets current git branch name
- **`{{ version_info() }}`** - Generates version information block
- **`{{ project_stats() }}`** - Generates project statistics
- **`{{ release_notes() }}`** - Generates release notes from metadata
- **`{{ project_info() }}`** - Generates project information block
- **`{{ build_info() }}`** - Generates build information table
- **`{{ contributors() }}`** - Lists contributors from git log
- **`{{ last_updated() }}`** - Gets last updated date from git

### Metadata File

The `.metadata.yaml` file contains project metadata that is synchronized with git tags:

```yaml
# Version information
version: "v1.0.0"
version_name: "Initial Release"
release_date: "2025-01-01"

# Project information
project:
  name: "Documentation Project"
  description: "Comprehensive documentation for your project"
  repository: "https://github.com/yourusername/your-project"
  documentation: "https://yourusername.github.io/your-project/"

# Release information
release:
  major_features:
    - "Initial documentation structure"
    - "Comprehensive user guide"
  improvements:
    - "Clean and modern design"
    - "Responsive layout for all devices"
```

### Usage Examples

In your markdown files, you can use macros like:

```markdown
# Welcome to {{ metadata.project.name }}

{{ version_info() }}

{{ project_info() }}

## Release Notes

{{ release_notes() }}

## Project Statistics

{{ project_stats() }}

## Build Information

{{ build_info() }}
```

### Environment Variables

The macros also set environment variables that can be used in templates:

- `git_tag` - Latest git tag
- `commit_hash` - Current commit hash
- `branch_name` - Current branch name
- `metadata` - Full metadata object
- `build_date` - Build timestamp
- `last_updated` - Last update date

## Template Versions

The template supports different complexity levels:

- **Basic**: Essential features for simple documentation
- **Standard**: Recommended configuration for most projects
- **Advanced**: Full-featured setup for complex projects

Choose the appropriate version based on your project needs and maintenance capacity.
