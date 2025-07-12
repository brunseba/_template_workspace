# Welcome to {{ metadata.project.name }}

{{ project_info() }}

## What is {{ metadata.project.name }}?

{{ metadata.project.description }}

{{ version_info() }}

## Quick Start

Get started with our documentation in just a few steps:

1. **Installation**: Follow our [installation guide](installation.md) to set up the project
2. **Configuration**: Learn how to configure the project for your needs
3. **Usage**: Explore our [user guide](user-guide/basic-usage.md) for examples and best practices
4. **API Reference**: Check out our comprehensive [API documentation](api-reference/overview.md)

## Key Features

{{ release_notes() }}

## Project Statistics

{{ project_stats() }}

## Latest Updates

**Current Version:** {{ git_tag }}  
**Last Updated:** {{ last_updated() }}  
**Build Date:** {{ build_date }}

## Repository Links

- **Source Code**: [{{ metadata.project.repository }}]({{ metadata.project.repository }})
- **Documentation**: [{{ metadata.project.documentation }}]({{ metadata.project.documentation }})
- **Issues & Support**: [{{ metadata.project.repository }}/issues]({{ metadata.project.repository }}/issues)

## Community

Join our community and contribute to the project:

{% if metadata.links %}
- **Homepage**: [{{ metadata.links.homepage }}]({{ metadata.links.homepage }})
- **Support**: [{{ metadata.links.support }}]({{ metadata.links.support }})
- **Community**: [{{ metadata.links.community }}]({{ metadata.links.community }})
{% endif %}

## Navigation

Explore our documentation:

- **[About](about.md)** - Learn more about the project
- **[Getting Started](getting-started/overview.md)** - Start your journey
- **[User Guide](user-guide/basic-usage.md)** - Comprehensive usage guide
- **[API Reference](api-reference/overview.md)** - Complete API documentation
- **[Development](development/setup.md)** - Contributing and development setup

---

!!! info "Documentation Status"
    This documentation is automatically built from version **{{ git_tag }}** (commit {{ commit_hash }}) and is always up-to-date with the latest changes.

*Generated on {{ build_date }}*
