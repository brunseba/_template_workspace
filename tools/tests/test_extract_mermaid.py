"""Tests for the extract_mermaid module."""
import os
import tempfile
import pytest
from pathlib import Path
from tools.extract_mermaid import extract_mermaid_blocks, process_file


class TestExtractMermaid:
    """Test cases for mermaid diagram extraction."""

    def test_extract_single_mermaid_diagram(self):
        """Test extracting a single mermaid diagram from markdown."""
        markdown_content = """
# Test Document

Some text here.

```mermaid
graph TD
    A[Start] --> B[Process]
    B --> C[End]
```

More text.
"""
        diagrams = extract_mermaid_blocks(markdown_content)
        assert len(diagrams) == 1
        assert "graph TD" in diagrams[0][1]
        assert "A[Start] --> B[Process]" in diagrams[0][1]

    def test_extract_multiple_mermaid_diagrams(self):
        """Test extracting multiple mermaid diagrams from markdown."""
        markdown_content = """
# Test Document

First diagram:

```mermaid
graph TD
    A --> B
```

Second diagram:

```mermaid
sequenceDiagram
    Alice->>Bob: Hello Bob, how are you?
    Bob-->>Alice: Great!
```
"""
        diagrams = extract_mermaid_blocks(markdown_content)
        assert len(diagrams) == 2
        assert "graph TD" in diagrams[0][1]
        assert "sequenceDiagram" in diagrams[1][1]

    def test_extract_no_mermaid_diagrams(self):
        """Test extracting from markdown with no mermaid diagrams."""
        markdown_content = """
# Test Document

Some text here.

```python
print("Hello, World!")
```

More text.
"""
        diagrams = extract_mermaid_blocks(markdown_content)
        assert len(diagrams) == 0

    def test_extract_empty_content(self):
        """Test extracting from empty content."""
        diagrams = extract_mermaid_blocks("")
        assert len(diagrams) == 0

    def test_extract_with_whitespace_and_indentation(self):
        """Test extracting diagrams with various whitespace and indentation."""
        markdown_content = """
# Test Document

```mermaid
    graph TD
        A[Start] --> B[Process]
        B --> C[End]
```
"""
        diagrams = extract_mermaid_blocks(markdown_content)
        assert len(diagrams) == 1
        # Should preserve indentation
        assert "graph TD" in diagrams[0][1]

    def test_process_file_with_valid_markdown(self):
        """Test processing a file with valid markdown and mermaid diagrams."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("""
# Test Document

```mermaid
graph TD
    A --> B
```
""")
            temp_file = f.name

        try:
            result = process_file(temp_file)
            assert result is not None
            assert len(result) == 1
            assert "graph TD" in result[0]
        finally:
            os.unlink(temp_file)

    def test_process_nonexistent_file(self):
        """Test processing a non-existent file."""
        result = process_file("/nonexistent/file.md")
        assert result is None

    def test_extract_mermaid_case_insensitive(self):
        """Test that mermaid code blocks are detected case-insensitively."""
        markdown_content = """
```MERMAID
graph TD
    A --> B
```

```Mermaid
sequenceDiagram
    Alice->>Bob: Hello
```
"""
        diagrams = extract_mermaid_diagrams(markdown_content)
        assert len(diagrams) == 2

    def test_extract_mermaid_with_extra_spaces(self):
        """Test extracting mermaid diagrams with extra spaces in code block declaration."""
        markdown_content = """
```  mermaid  
graph TD
    A --> B
```
"""
        diagrams = extract_mermaid_diagrams(markdown_content)
        assert len(diagrams) == 1
        assert "graph TD" in diagrams[0]

    def test_extract_complex_mermaid_diagram(self):
        """Test extracting a complex mermaid diagram."""
        markdown_content = """
```mermaid
flowchart TD
    A[Christmas] -->|Get money| B(Go shopping)
    B --> C{Let me think}
    C -->|One| D[Laptop]
    C -->|Two| E[iPhone]
    C -->|Three| F[fa:fa-car Car]
    D --> G[Result 1]
    E --> G
    F --> G
```
"""
        diagrams = extract_mermaid_diagrams(markdown_content)
        assert len(diagrams) == 1
        assert "flowchart TD" in diagrams[0]
        assert "fa:fa-car Car" in diagrams[0]
