# Macro Usage Examples

This page demonstrates how to use the various macros available in the template.

## Basic Information Macros

### Project Name
The project name is: **{{ metadata.project.name }}**

### Current Version
We're running version: **{{ get_git_tag() }}**

### Git Information
- **Branch:** {{ get_branch_name() }}
- **Commit:** {{ get_commit_hash() }}
- **Last Updated:** {{ last_updated() }}

## Information Blocks

### Version Information Block
{{ version_info() }}

### Project Information Block
{{ project_info() }}

## Statistics and Metrics

### Project Statistics
{{ project_stats() }}

### Build Information Table
{{ build_info() }}

## Release Information

### Release Notes
{{ release_notes() }}

## Contributors

### Project Contributors
{{ contributors() }}

## Raw Metadata Access

You can also access metadata directly:

- **Repository:** {{ metadata.project.repository }}
- **Documentation:** {{ metadata.project.documentation }}
- **Description:** {{ metadata.project.description }}

### Conditional Content

{% if metadata.links %}
#### External Links Available:
- Homepage: {{ metadata.links.homepage }}
- Support: {{ metadata.links.support }}
- Community: {{ metadata.links.community }}
{% else %}
No external links configured.
{% endif %}

### Authors Information

{% if metadata.authors %}
#### Project Authors:
{% for author in metadata.authors %}
- **{{ author.name }}** ({{ author.role }}) - {{ author.email }}
{% endfor %}
{% else %}
No authors information available.
{% endif %}

### Settings Information

{% if metadata.settings %}
#### Project Settings:
- **Theme:** {{ metadata.settings.theme }}
- **Primary Color:** {{ metadata.settings.primary_color }}
- **Search Enabled:** {{ metadata.settings.enable_search }}
{% endif %}

## Environment Variables

The following environment variables are available:

- **git_tag:** `{{ git_tag }}`
- **commit_hash:** `{{ commit_hash }}`
- **branch_name:** `{{ branch_name }}`
- **build_date:** `{{ build_date }}`

## Function Calls

You can also call functions directly:

- **get_git_tag():** `{{ get_git_tag() }}`
- **get_commit_hash():** `{{ get_commit_hash() }}`
- **get_branch_name():** `{{ get_branch_name() }}`
- **last_updated():** `{{ last_updated() }}`

## Tips for Using Macros

1. **Always use double curly braces** for macro calls: `{{ macro_name() }}`
2. **Use dot notation** for accessing nested metadata: `{{ metadata.project.name }}`
3. **Use conditional blocks** for optional content: `{% if metadata.links %}...{% endif %}`
4. **Loop through arrays** with for loops: `{% for item in metadata.array %}...{% endfor %}`

---

*This page demonstrates the power of MkDocs macros for dynamic content generation.*
