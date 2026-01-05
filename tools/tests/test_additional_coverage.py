"""Additional test coverage for edge cases and error handling."""
import os
import tempfile
import pytest
from pathlib import Path
from click.testing import CliRunner
from tools.extract_mermaid import (
    extract_mermaid_blocks, 
    extract_mermaid_diagrams,
    find_markdown_files,
    generate_mmd_files,
    preview_extraction,
    create_drawio_xml
)
from tools.mermaid_to_drawio import (
    generate_drawio_file,
    convert_mermaid_to_drawio,
    process_mermaid_files,
    escape_for_xml,
    create_mermaid_data_json,
    get_diagram_name_from_filename
)
from tools.cli import cli


class TestAdditionalCoverage:
    """Test cases for additional code coverage."""

    def test_extract_mermaid_blocks_empty_input(self):
        """Test extracting from empty input."""
        result = extract_mermaid_blocks("")
        assert result == []

    def test_extract_mermaid_blocks_no_mermaid(self):
        """Test extracting from content without mermaid blocks."""
        content = """
        # Regular markdown
        
        ```python
        print("hello")
        ```
        
        Some text.
        """
        result = extract_mermaid_blocks(content)
        assert result == []

    def test_extract_mermaid_blocks_case_insensitive(self):
        """Test case insensitive mermaid block detection."""
        content = """
        ```MERMAID
        graph TD
            A --> B
        ```
        
        ```Mermaid
        sequenceDiagram
            Alice->>Bob: Hello
        ```
        """
        result = extract_mermaid_blocks(content)
        assert len(result) == 2
        assert "graph TD" in result[0][1]
        assert "sequenceDiagram" in result[1][1]

    def test_extract_mermaid_blocks_with_spaces(self):
        """Test mermaid blocks with extra spaces."""
        content = """
        ```  mermaid  
        graph TD
            A --> B
        ```
        """
        result = extract_mermaid_blocks(content)
        assert len(result) == 1
        assert "graph TD" in result[0][1]

    def test_extract_mermaid_diagrams_wrapper(self):
        """Test the extract_mermaid_diagrams wrapper function."""
        content = """
        ```mermaid
        graph TD
            A --> B
        ```
        
        ```mermaid
        sequenceDiagram
            Alice->>Bob: Hello
        ```
        """
        result = extract_mermaid_diagrams(content)
        assert len(result) == 2
        assert "graph TD" in result[0]
        assert "sequenceDiagram" in result[1]

    def test_find_markdown_files_single_file(self):
        """Test finding markdown files with single file input."""
        with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as temp_file:
            temp_file.write(b"# Test")
            temp_file_path = temp_file.name
        
        try:
            result = find_markdown_files(Path(temp_file_path))
            assert len(result) == 1
            assert result[0] == Path(temp_file_path)
        finally:
            os.unlink(temp_file_path)

    def test_find_markdown_files_directory(self):
        """Test finding markdown files in directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create markdown files
            md_file1 = Path(temp_dir) / "test1.md"
            md_file2 = Path(temp_dir) / "test2.markdown"
            txt_file = Path(temp_dir) / "test.txt"
            
            md_file1.write_text("# Test 1")
            md_file2.write_text("# Test 2")
            txt_file.write_text("Not markdown")
            
            result = find_markdown_files(Path(temp_dir))
            assert len(result) == 2
            assert md_file1 in result
            assert md_file2 in result

    def test_find_markdown_files_recursive(self):
        """Test finding markdown files recursively."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create subdirectory
            subdir = Path(temp_dir) / "subdir"
            subdir.mkdir()
            
            # Create markdown files
            md_file1 = Path(temp_dir) / "test1.md"
            md_file2 = subdir / "test2.md"
            
            md_file1.write_text("# Test 1")
            md_file2.write_text("# Test 2")
            
            result = find_markdown_files(Path(temp_dir), recursive=True)
            assert len(result) == 2
            assert md_file1 in result
            assert md_file2 in result

    def test_find_markdown_files_non_markdown(self):
        """Test finding markdown files with non-markdown file."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_file:
            temp_file.write(b"Not markdown")
            temp_file_path = temp_file.name
        
        try:
            result = find_markdown_files(Path(temp_file_path))
            assert len(result) == 0
        finally:
            os.unlink(temp_file_path)

    def test_generate_mmd_files_success(self):
        """Test successful generation of mmd files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create markdown file with mermaid
            md_file = Path(temp_dir) / "test.md"
            md_file.write_text("""
            # Test
            
            ```mermaid
            graph TD
                A --> B
            ```
            
            ```mermaid
            sequenceDiagram
                Alice->>Bob: Hello
            ```
            """)
            
            output_dir = Path(temp_dir) / "output"
            result = generate_mmd_files(md_file, output_dir, verbose=True)
            
            assert result == 2
            assert (output_dir / "test_graph_TD.mmd").exists()
            assert (output_dir / "test_sequenceDiagram.mmd").exists()

    def test_generate_mmd_files_no_diagrams(self):
        """Test generation with no mermaid diagrams."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create markdown file without mermaid
            md_file = Path(temp_dir) / "test.md"
            md_file.write_text("# Test\n\nNo mermaid here.")
            
            output_dir = Path(temp_dir) / "output"
            result = generate_mmd_files(md_file, output_dir)
            
            assert result == 0

    def test_generate_mmd_files_duplicate_types(self):
        """Test generation with duplicate diagram types."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create markdown file with duplicate diagram types
            md_file = Path(temp_dir) / "test.md"
            md_file.write_text("""
            ```mermaid
            graph TD
                A --> B
            ```
            
            ```mermaid
            graph TD
                C --> D
            ```
            """)
            
            output_dir = Path(temp_dir) / "output"
            result = generate_mmd_files(md_file, output_dir)
            
            assert result == 2
            assert (output_dir / "test_graph_TD.mmd").exists()
            assert (output_dir / "test_graph_TD_2.mmd").exists()

    def test_preview_extraction(self):
        """Test preview extraction functionality."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create markdown file with mermaid
            md_file = Path(temp_dir) / "test.md"
            md_file.write_text("""
            ```mermaid
            graph TD
                A --> B
            ```
            """)
            
            output_dir = Path(temp_dir) / "output"
            result = preview_extraction(md_file, output_dir)
            
            assert result == 1

    def test_preview_extraction_no_diagrams(self):
        """Test preview extraction with no diagrams."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create markdown file without mermaid
            md_file = Path(temp_dir) / "test.md"
            md_file.write_text("# Test\n\nNo mermaid here.")
            
            output_dir = Path(temp_dir) / "output"
            result = preview_extraction(md_file, output_dir)
            
            assert result == 0

    def test_create_drawio_xml(self):
        """Test creating drawio XML from mmd files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create mmd files
            mmd_file1 = Path(temp_dir) / "test1.mmd"
            mmd_file2 = Path(temp_dir) / "test2.mmd"
            
            mmd_file1.write_text("graph TD\n    A --> B")
            mmd_file2.write_text("sequenceDiagram\n    Alice->>Bob: Hello")
            
            output_file = Path(temp_dir) / "output.drawio"
            create_drawio_xml([mmd_file1, mmd_file2], output_file)
            
            assert output_file.exists()
            content = output_file.read_text()
            assert '<mxfile' in content
            assert '</mxfile>' in content

    def test_escape_for_xml(self):
        """Test XML escaping functionality."""
        result = escape_for_xml("Test & <content> with \"quotes\"")
        assert "&amp;" in result
        assert "&lt;" in result
        assert "&gt;" in result
        assert "&quot;" in result

    def test_create_mermaid_data_json(self):
        """Test creating mermaid data JSON."""
        content = "graph TD\n    A --> B"
        result = create_mermaid_data_json(content)
        assert '"data"' in result
        assert "graph TD" in result

    def test_get_diagram_name_from_filename(self):
        """Test getting diagram name from filename."""
        assert get_diagram_name_from_filename("test_graph_TD.mmd") == "Test Graph Td"
        assert get_diagram_name_from_filename("example_sequenceDiagram.mmd") == "Sequencediagram"
        assert get_diagram_name_from_filename("mermaid-example_flowchart.mmd") == "Flowchart"

    def test_process_mermaid_files_success(self):
        """Test processing mermaid files successfully."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create mmd files
            mmd_file1 = os.path.join(temp_dir, "test1.mmd")
            mmd_file2 = os.path.join(temp_dir, "test2.mmd")
            
            with open(mmd_file1, 'w') as f:
                f.write("graph TD\n    A --> B")
            
            with open(mmd_file2, 'w') as f:
                f.write("sequenceDiagram\n    Alice->>Bob: Hello")
            
            result = process_mermaid_files(temp_dir)
            
            assert len(result) == 2
            assert mmd_file1 in result
            assert mmd_file2 in result

    def test_process_mermaid_files_empty_directory(self):
        """Test processing empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = process_mermaid_files(temp_dir)
            assert result == []

    def test_process_mermaid_files_nonexistent_directory(self):
        """Test processing nonexistent directory."""
        result = process_mermaid_files("/nonexistent/directory")
        assert result == []

    def test_convert_mermaid_to_drawio_success(self):
        """Test converting mermaid to drawio successfully."""
        mermaid_content = "graph TD\n    A --> B"
        result = convert_mermaid_to_drawio(mermaid_content)
        
        assert result.startswith('<?xml version="1.0"')
        assert '<mxfile' in result
        assert '</mxfile>' in result

    def test_convert_mermaid_to_drawio_empty(self):
        """Test converting empty mermaid content."""
        result = convert_mermaid_to_drawio("")
        
        assert result.startswith('<?xml version="1.0"')
        assert '<mxfile' in result

    def test_convert_mermaid_to_drawio_complex(self):
        """Test converting complex mermaid diagram."""
        mermaid_content = """
        flowchart TD
            A[Christmas] -->|Get money| B(Go shopping)
            B --> C{Let me think}
            C -->|One| D[Laptop]
            C -->|Two| E[iPhone]
            C -->|Three| F[fa:fa-car Car]
        """
        result = convert_mermaid_to_drawio(mermaid_content)
        
        assert result.startswith('<?xml version="1.0"')
        assert '<mxfile' in result
        assert '</mxfile>' in result

    def test_cli_extract_with_recursive_flag(self):
        """Test CLI extract command with recursive flag."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create subdirectory with markdown file
            subdir = os.path.join(temp_dir, "subdir")
            os.makedirs(subdir)
            
            md_file = os.path.join(subdir, "test.md")
            with open(md_file, 'w') as f:
                f.write("""
                # Test
                
                ```mermaid
                graph TD
                    A --> B
                ```
                """)
            
            result = runner.invoke(cli, ['extract', temp_dir, '--recursive'])
            
            assert result.exit_code == 0
            assert "Generated" in result.output or "Summary" in result.output

    def test_cli_extract_with_dry_run(self):
        """Test CLI extract command with dry run."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            md_file = os.path.join(temp_dir, "test.md")
            with open(md_file, 'w') as f:
                f.write("""
                ```mermaid
                graph TD
                    A --> B
                ```
                """)
            
            result = runner.invoke(cli, ['extract', temp_dir, '--dry-run'])
            
            assert result.exit_code == 0
            assert "Would extract" in result.output or "Found" in result.output

    def test_cli_extract_with_verbose(self):
        """Test CLI extract command with verbose output."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            md_file = os.path.join(temp_dir, "test.md")
            with open(md_file, 'w') as f:
                f.write("""
                ```mermaid
                graph TD
                    A --> B
                ```
                """)
            
            result = runner.invoke(cli, ['extract', temp_dir, '--verbose'])
            
            assert result.exit_code == 0

    def test_cli_md_to_drawio_basic(self):
        """Test CLI md-to-drawio command basic functionality."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            md_file = os.path.join(temp_dir, "test.md")
            with open(md_file, 'w') as f:
                f.write("""
                ```mermaid
                graph TD
                    A --> B
                ```
                """)
            
            result = runner.invoke(cli, ['md-to-drawio', md_file])
            
            assert result.exit_code == 0
            assert "Generated" in result.output

    def test_cli_md_to_drawio_with_options(self):
        """Test CLI md-to-drawio command with various options."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            md_file = os.path.join(temp_dir, "test.md")
            with open(md_file, 'w') as f:
                f.write("""
                ```mermaid
                graph TD
                    A --> B
                ```
                """)
            
            result = runner.invoke(cli, ['md-to-drawio', md_file, '--verbose', '--keep-temp'])
            
            assert result.exit_code == 0
