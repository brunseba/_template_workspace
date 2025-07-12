# Contributing to {{ metadata.project.name }}

Thank you for your interest in contributing to {{ metadata.project.name }}! We welcome contributions from the community and are grateful for any improvements you can provide.

{{ project_info() }}

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Community](#community)

---

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- ✅ Using welcoming and inclusive language
- ✅ Being respectful of differing viewpoints and experiences
- ✅ Gracefully accepting constructive criticism
- ✅ Focusing on what is best for the community
- ✅ Showing empathy towards other community members

---

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**: Check with `python --version`
- **Git**: Version control system
- **pip**: Python package manager
- **Node.js** (optional): For frontend contributions

### Fork and Clone

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/yourusername/{{ metadata.project.name.lower().replace(' ', '-') }}.git
   cd {{ metadata.project.name.lower().replace(' ', '-') }}
   ```

3. **Add upstream** remote:
   ```bash
   git remote add upstream {{ metadata.project.repository }}.git
   ```

---

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

#### 🐛 Bug Reports
- Use the bug report template
- Include steps to reproduce
- Provide system information
- Include error messages and logs

#### 💡 Feature Requests
- Use the feature request template
- Explain the problem you're solving
- Describe your proposed solution
- Consider alternative approaches

#### 📖 Documentation
- Fix typos and improve clarity
- Add examples and use cases
- Translate documentation
- Improve API documentation

#### 🔧 Code Contributions
- Bug fixes
- New features
- Performance improvements
- Test coverage improvements

#### 🎨 Design
- UI/UX improvements
- Icon and graphic design
- Accessibility improvements

---

## Development Setup

### Local Environment

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

4. **Run tests** to verify setup:
   ```bash
   pytest
   ```

### Development Tools

We use the following tools for development:

- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pytest**: Testing framework
- **Pre-commit**: Git hooks

---

## Coding Standards

### Python Code Style

- Follow **PEP 8** style guide
- Use **Black** for code formatting
- Maximum line length: **88 characters**
- Use **type hints** for function signatures
- Write **docstrings** for all public functions

### Code Example

```python
def calculate_metrics(data: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculate project metrics from data.
    
    Args:
        data: List of data dictionaries containing metrics
        
    Returns:
        Dictionary with calculated metrics
        
    Raises:
        ValueError: If data is empty or invalid
    """
    if not data:
        raise ValueError("Data cannot be empty")
    
    # Your implementation here
    return {"total": len(data)}
```

### Documentation Standards

- Use **Markdown** for documentation
- Include **code examples** where appropriate
- Keep documentation **up-to-date** with code changes
- Use **clear headings** and **consistent formatting**

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_example.py

# Run tests in parallel
pytest -n auto
```

### Writing Tests

- Write tests for **all new features**
- Maintain **high test coverage** (aim for >90%)
- Use **descriptive test names**
- Include **both positive and negative** test cases

### Test Example

```python
def test_calculate_metrics_with_valid_data():
    """Test metrics calculation with valid data."""
    data = [{"type": "doc", "lines": 100}]
    result = calculate_metrics(data)
    assert result["total"] == 1

def test_calculate_metrics_with_empty_data():
    """Test metrics calculation with empty data raises ValueError."""
    with pytest.raises(ValueError, match="Data cannot be empty"):
        calculate_metrics([])
```

---

## Documentation

### Building Documentation

```bash
# Build documentation
mkdocs build

# Serve documentation locally
mkdocs serve

# Deploy documentation
mkdocs gh-deploy
```

### Documentation Guidelines

- Update documentation **with every code change**
- Include **practical examples**
- Use **screenshots** for UI changes
- Keep **README** and **API docs** current

---

## Pull Request Process

### Before Submitting

1. **Update** your fork:
   ```bash
   git checkout main
   git pull upstream main
   git push origin main
   ```

2. **Create** a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make** your changes and commit:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

### Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples**:
- `feat: add user authentication`
- `fix: resolve login redirect issue`
- `docs: update API documentation`

### Pull Request Checklist

- [ ] **Tests** pass locally
- [ ] **Code** follows style guidelines
- [ ] **Documentation** is updated
- [ ] **Commit messages** follow conventional format
- [ ] **PR description** explains changes clearly
- [ ] **Breaking changes** are documented

### Review Process

1. **Automated checks** must pass
2. **At least one maintainer** review required
3. **All conversations** must be resolved
4. **Documentation** must be updated
5. **Tests** must pass

---

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Pull Requests**: Code contributions
- **Email**: Direct contact for sensitive issues

### Getting Help

- Check **existing issues** before creating new ones
- Use **discussion** for questions
- Read **documentation** first
- Provide **detailed information** when asking for help

### Recognition

Contributors are recognized in:

- **Changelog**: All contributors listed
- **GitHub**: Contributor graphs and statistics
- **Documentation**: Hall of fame section
- **Releases**: Special thanks in release notes

---

## Project Statistics

{{ project_stats() }}

## Build Information

{{ build_info() }}

---

## License

By contributing to {{ metadata.project.name }}, you agree that your contributions will be licensed under the same license as the project. See [LICENSE](license.md) for details.

---

## Questions?

If you have questions about contributing, please:

1. **Check** existing [issues]({{ metadata.project.repository }}/issues) and [discussions]({{ metadata.project.repository }}/discussions)
2. **Create** a new discussion for general questions
3. **Contact** maintainers for specific concerns

Thank you for contributing to {{ metadata.project.name }}! 🎉

---

*Contributing guide last updated: {{ last_updated() }}*
