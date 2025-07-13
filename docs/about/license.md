# License

## {{ metadata.project.name }} License

{{ project_info() }}

---

## MIT License

Copyright (c) {% if metadata.authors %}{% for author in metadata.authors %}{{ author.name }}{% if not loop.last %}, {% endif %}{% endfor %}{% else %}{{ metadata.project.name }} Contributors{% endif %}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Third-Party Licenses

This project uses several open-source libraries and tools. Below are their respective licenses:

### MkDocs

- **License**: BSD 2-Clause License
- **Repository**: [https://github.com/mkdocs/mkdocs](https://github.com/mkdocs/mkdocs)
- **Copyright**: Copyright (c) 2014, Tom Christie

### Material for MkDocs

- **License**: MIT License
- **Repository**: [https://github.com/squidfunk/mkdocs-material](https://github.com/squidfunk/mkdocs-material)
- **Copyright**: Copyright (c) 2016-2024 Martin Donath

### MkDocs Plugins

The following MkDocs plugins are used in this project:

| Plugin | License | Repository |
|--------|---------|------------|
| mkdocs-macros-plugin | MIT | [https://github.com/fralau/mkdocs_macros_plugin](https://github.com/fralau/mkdocs_macros_plugin) |
| mkdocs-git-revision-date-localized-plugin | MIT | [https://github.com/timvink/mkdocs-git-revision-date-localized-plugin](https://github.com/timvink/mkdocs-git-revision-date-localized-plugin) |
| mkdocs-git-committers-plugin | MIT | [https://github.com/byrnereese/mkdocs-git-committers-plugin](https://github.com/byrnereese/mkdocs-git-committers-plugin) |
| mkdocs-mermaid2-plugin | MIT | [https://github.com/fralau/mkdocs-mermaid2-plugin](https://github.com/fralau/mkdocs-mermaid2-plugin) |

### Dependencies

This project also depends on various Python packages and JavaScript libraries. For a complete list of dependencies and their licenses, please refer to:

- `requirements.txt` for Python dependencies
- `package.json` for JavaScript dependencies (if applicable)

## Attribution

If you use this project or its documentation template, we appreciate attribution. You can include the following notice:

> Documentation generated using the MkDocs Template Suite  
> Template repository: [https://github.com/yourusername/mkdocs-template](https://github.com/yourusername/mkdocs-template)

## License Compliance

This project is committed to open-source license compliance. If you believe there is a license issue or if you have questions about licensing, please:

1. **Review our dependencies**: Check the `requirements.txt` and documentation for all third-party licenses
2. **Contact us**: Open an issue in our [repository]({{ metadata.project.repository }}/issues) with license concerns
3. **Contribute**: Help us maintain license compliance by reporting any issues

## Usage Rights

Under the MIT License, you are free to:

- ✅ **Use** this software for any purpose, including commercial use
- ✅ **Modify** the software to fit your needs
- ✅ **Distribute** copies of the software
- ✅ **Sublicense** the software
- ✅ **Sell** copies of the software

## Obligations

When using this software, you must:

- 📋 **Include** the original copyright notice and license text
- 📋 **Preserve** any existing license notices in the code
- 📋 **Not hold** the original authors liable for any damages

## Disclaimer

This software is provided "as is" without warranty. The authors are not responsible for any damages or issues that may arise from using this software.

---

## Version Information

{{ version_info() }}

**Last Updated**: {{ last_updated() }}

For the most current license information, please visit our [repository]({{ metadata.project.repository }}).

---

*This license page was generated using MkDocs macros from project metadata.*
