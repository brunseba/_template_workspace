# Navigation Guide

This guide helps you navigate through the {{ metadata.project.name }} documentation effectively.

{{ project_info() }}

---

## Documentation Structure

Our documentation is organized into logical sections to help you find information quickly:

### 🏠 Home
- **[Overview](index.md)**: Main landing page with project introduction
- **[Navigation Guide](navigation.md)**: This page - how to use the documentation
- **[Documentation Summary](README.md)**: Complete overview of all sections

### 🚀 Getting Started
- **[System Overview](getting-started/overview.md)**: High-level system overview
- **[Quick Setup](getting-started/quick-start.md)**: Get up and running quickly
- **[Installation](getting-started/installation.md)**: Detailed installation instructions
- **[Configuration](getting-started/configuration.md)**: Initial configuration steps

### 📚 User Guide
- **[Basic Usage](user-guide/basic-usage.md)**: Essential features and functions
- **[Advanced Usage](user-guide/advanced-usage.md)**: Power user features
- **[Best Practices](user-guide/best-practices.md)**: Recommended approaches
- **[Troubleshooting](user-guide/troubleshooting.md)**: Common issues and solutions

### 🏛️ Architecture
- **[System Architecture](architecture/system-architecture.md)**: Overall system design
- **[Security Design](architecture/security-design.md)**: Security considerations
- **[Technical Design](architecture/technical-design.md)**: Technical implementation details

### 🔌 API Reference
- **[API Overview](api-reference/overview.md)**: API introduction and concepts
- **[Endpoints](api-reference/endpoints.md)**: Complete endpoint documentation
- **[Data Models](api-reference/data-models.md)**: Data structures and schemas
- **[Use Cases](api-reference/use-cases.md)**: Common API usage patterns

### 💻 Development
- **[Setup Guide](development/setup.md)**: Development environment setup
- **[Contributing](development/contributing.md)**: How to contribute to the project
- **[Testing](development/testing.md)**: Testing guidelines and practices
- **[CI/CD](development/cicd.md)**: Continuous integration and deployment

### 🚀 Deployment
- **[Installation Guide](deployment/installation.md)**: Production installation
- **[Kubernetes](deployment/kubernetes.md)**: Kubernetes deployment
- **[Docker](deployment/docker.md)**: Docker containerization
- **[Configuration](deployment/configuration.md)**: Production configuration

### 📊 Examples
- **[Basic Examples](examples/basic-examples.md)**: Simple usage examples
- **[Advanced Examples](examples/advanced-examples.md)**: Complex scenarios
- **[Use Cases](examples/use-cases.md)**: Real-world applications

### 📖 Reference
- **[CLI Commands](reference/cli-commands.md)**: Command-line interface reference
- **[Configuration](reference/configuration.md)**: Configuration options
- **[Troubleshooting](reference/troubleshooting.md)**: Problem resolution
- **[FAQ](reference/faq.md)**: Frequently asked questions

### 📋 About
- **[About Project](about.md)**: Project information and team
- **[Changelog](changelog.md)**: Version history and changes
- **[License](license.md)**: Legal information and licenses
- **[Contributing](contributing.md)**: Contribution guidelines

---

## Navigation Tips

### 🔍 Search Functionality
- Use the **search bar** at the top of the page
- Search supports **partial matches** and **keywords**
- Results show **page context** for relevance

### 📱 Mobile Navigation
- **Hamburger menu** on mobile devices
- **Swipe gestures** supported
- **Touch-friendly** interface elements

### ⌨️ Keyboard Shortcuts
- **`/`**: Focus search bar
- **`Esc`**: Close search/navigation
- **Arrow keys**: Navigate search results

### 🔗 Cross-References
- **Internal links** are highlighted in blue
- **External links** open in new tabs
- **Broken links** are marked for easy identification

### 🏷️ Content Tags
- **📖 Documentation**: General documentation pages
- **🔧 API**: API-related content
- **📚 Tutorial**: Step-by-step guides
- **📝 Guide**: How-to instructions
- **📋 Reference**: Reference materials
- **💡 Examples**: Code and usage examples

---

## Getting Help

### 🎯 Finding Specific Information

1. **Start with the overview**: Read the [main page](index.md) for context
2. **Check Getting Started**: If you're new, begin with [Quick Setup](getting-started/quick-start.md)
3. **Use search**: Type keywords related to your question
4. **Browse by category**: Use the navigation sections above
5. **Check examples**: Look at [Examples](examples/basic-examples.md) for practical guidance

### 🔄 Staying Updated

- **Bookmark** frequently used pages
- **Check the [Changelog](changelog.md)** for updates
- **Subscribe** to repository notifications
- **Follow** project announcements

### 📞 Getting Support

If you can't find what you're looking for:

1. **Search existing issues**: Check [GitHub Issues]({{ metadata.project.repository }}/issues)
2. **Join discussions**: Participate in [GitHub Discussions]({{ metadata.project.repository }}/discussions)
3. **Ask questions**: Create a new issue with the "question" label
4. **Contact maintainers**: See [About](about.md) for contact information

---

## Documentation Features

### 🎨 Visual Elements
- **Emojis** for easy section identification
- **Code highlighting** with syntax support
- **Diagrams** using Mermaid
- **Tables** for structured information
- **Admonitions** for important notes

### 📊 Dynamic Content
This documentation uses dynamic content generation:

- **Version information**: {{ get_git_tag() }}
- **Last updated**: {{ last_updated() }}
- **Build date**: {{ build_date }}
- **Contributors**: Automatically generated from git history

### 🔄 Content Updates
Documentation is automatically updated when:

- **Code changes** are committed
- **Version tags** are created
- **Documentation files** are modified
- **Metadata** is updated

---

## Feedback and Improvements

### 📝 Documentation Feedback
Help us improve this documentation:

- **Report errors**: Found a mistake? [Open an issue]({{ metadata.project.repository }}/issues)
- **Suggest improvements**: Ideas for better organization or content
- **Contribute**: Submit pull requests with improvements
- **Rate pages**: Use the feedback buttons (when available)

### 🎯 What Makes Good Documentation
We strive for documentation that is:

- **Clear**: Easy to understand
- **Complete**: Covers all necessary topics
- **Current**: Up-to-date with latest changes
- **Consistent**: Uniform style and format
- **Accessible**: Works for all users

---

## Project Information

{{ build_info() }}

{{ project_stats() }}

---

*Navigation guide last updated: {{ last_updated() }}*

For more detailed information about the project, visit the [About](about.md) page.
