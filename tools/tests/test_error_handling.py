"""Tests for error handling and edge cases."""
import os
import tempfile
import pytest
from pathlib import Path
from click.testing import CliRunner
from tools.extract_mermaid import generate_mmd_files, find_markdown_files
from tools.mermaid_to_drawio import generate_drawio_file
from tools.cli import cli
from unittest.mock import patch, mock_open


class TestErrorHandling:
    """Test cases for error handling scenarios."""

    def test_generate_mmd_files_read_error(self):
        """Test handling of file read errors."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a file that will cause read error
            md_file = Path(temp_dir) / "test.md"
            md_file.write_text("# Test")
            
            # Mock read_text to raise an exception
            with patch.object(Path, 'read_text', side_effect=OSError("Permission denied")):
                output_dir = Path(temp_dir) / "output"
                with pytest.raises(SystemExit):  # click.ClickException causes SystemExit
                    generate_mmd_files(md_file, output_dir)

    def test_generate_mmd_files_write_error(self):
        """Test handling of file write errors."""
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
            
            # Mock write_text to raise an exception
            with patch.object(Path, 'write_text', side_effect=OSError("Disk full")):
                result = generate_mmd_files(md_file, output_dir)
                # Should still return count of diagrams found, but fail to write
                assert result == 1  # Found 1 diagram but couldn't write

    def test_generate_mmd_files_mkdir_error(self):
        """Test handling of directory creation errors."""
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
            
            # Mock mkdir to raise an exception
            with patch.object(Path, 'mkdir', side_effect=OSError("Permission denied")):
                with pytest.raises(SystemExit):  # click.ClickException causes SystemExit
                    generate_mmd_files(md_file, output_dir)

    def test_generate_drawio_file_with_verbose_error(self):
        """Test generate_drawio_file with verbose output and file errors."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a non-existent mermaid file
            mmd_file = os.path.join(temp_dir, "nonexistent.mmd")
            output_file = os.path.join(temp_dir, "output.drawio")
            
            # Should handle missing file gracefully with verbose output
            generate_drawio_file([mmd_file], output_file, verbose=True)
            
            # Should not create output file if no valid input files
            assert not os.path.exists(output_file)

    def test_generate_drawio_file_read_error(self):
        """Test generate_drawio_file with file read errors."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create mermaid file
            mmd_file = os.path.join(temp_dir, "test.mmd")
            with open(mmd_file, 'w') as f:
                f.write("graph TD\n    A --> B")
            
            output_file = os.path.join(temp_dir, "output.drawio")
            
            # Mock open to raise an exception for reading
            with patch('builtins.open', side_effect=OSError("Permission denied")):
                generate_drawio_file([mmd_file], output_file, verbose=True)
                
                # Should not create output file if can't read input
                assert not os.path.exists(output_file)

    def test_generate_drawio_file_write_error(self):
        """Test generate_drawio_file with file write errors."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create mermaid file
            mmd_file = os.path.join(temp_dir, "test.mmd")
            with open(mmd_file, 'w') as f:
                f.write("graph TD\n    A --> B")
            
            output_file = os.path.join(temp_dir, "output.drawio")
            
            # Mock open to raise an exception for writing
            def mock_open_side_effect(filename, mode='r', *args, **kwargs):
                if 'w' in mode and filename == output_file:
                    raise OSError("Disk full")
                return mock_open(read_data="graph TD\n    A --> B")(filename, mode, *args, **kwargs)
            
            with patch('builtins.open', side_effect=mock_open_side_effect):
                with pytest.raises(SystemExit):  # sys.exit(1) called on write error
                    generate_drawio_file([mmd_file], output_file)

    def test_cli_extract_with_invalid_output_dir(self):
        """Test CLI extract with invalid output directory."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create markdown file
            md_file = os.path.join(temp_dir, "test.md")
            with open(md_file, 'w') as f:
                f.write("""
                ```mermaid
                graph TD
                    A --> B
                ```
                """)
            
            # Try to use a file as output directory
            invalid_output = os.path.join(temp_dir, "not_a_dir.txt")
            with open(invalid_output, 'w') as f:
                f.write("This is a file, not a directory")
            
            result = runner.invoke(cli, ['extract', temp_dir, '--output-dir', invalid_output])
            
            # Should handle the error gracefully
            assert result.exit_code != 0

    def test_cli_to_drawio_with_files_option(self):
        """Test CLI to-drawio with specific files option."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create mermaid files
            mmd_file1 = os.path.join(temp_dir, "test1.mmd")
            mmd_file2 = os.path.join(temp_dir, "test2.mmd")
            
            with open(mmd_file1, 'w') as f:
                f.write("graph TD\n    A --> B")
            
            with open(mmd_file2, 'w') as f:
                f.write("sequenceDiagram\n    Alice->>Bob: Hello")
            
            result = runner.invoke(cli, ['to-drawio', '--files', mmd_file1, mmd_file2])
            
            assert result.exit_code == 0
            assert "Generated" in result.output or "Created" in result.output

    def test_cli_to_drawio_with_verbose(self):
        """Test CLI to-drawio with verbose output."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create mermaid file
            mmd_file = os.path.join(temp_dir, "test.mmd")
            with open(mmd_file, 'w') as f:
                f.write("graph TD\n    A --> B")
            
            result = runner.invoke(cli, ['to-drawio', temp_dir, '--verbose'])
            
            assert result.exit_code == 0

    def test_cli_md_to_drawio_with_separate_files(self):
        """Test CLI md-to-drawio with separate files option."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create markdown files
            md_file1 = os.path.join(temp_dir, "test1.md")
            md_file2 = os.path.join(temp_dir, "test2.md")
            
            with open(md_file1, 'w') as f:
                f.write("""
                ```mermaid
                graph TD
                    A --> B
                ```
                """)
            
            with open(md_file2, 'w') as f:
                f.write("""
                ```mermaid
                sequenceDiagram
                    Alice->>Bob: Hello
                ```
                """)
            
            result = runner.invoke(cli, ['md-to-drawio', temp_dir, '--separate-files'])
            
            assert result.exit_code == 0
            assert "Generated" in result.output

    def test_cli_md_to_drawio_with_recursive(self):
        """Test CLI md-to-drawio with recursive option."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create subdirectory
            subdir = os.path.join(temp_dir, "subdir")
            os.makedirs(subdir)
            
            # Create markdown file in subdirectory
            md_file = os.path.join(subdir, "test.md")
            with open(md_file, 'w') as f:
                f.write("""
                ```mermaid
                graph TD
                    A --> B
                ```
                """)
            
            result = runner.invoke(cli, ['md-to-drawio', temp_dir, '--recursive'])
            
            assert result.exit_code == 0
            assert "Generated" in result.output

    def test_cli_md_to_drawio_no_diagrams(self):
        """Test CLI md-to-drawio with no diagrams found."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create markdown file without diagrams
            md_file = os.path.join(temp_dir, "test.md")
            with open(md_file, 'w') as f:
                f.write("# Test\n\nNo diagrams here.")
            
            result = runner.invoke(cli, ['md-to-drawio', md_file])
            
            assert result.exit_code == 0
            assert "No Mermaid diagrams found" in result.output

    def test_find_markdown_files_warning(self):
        """Test find_markdown_files with non-markdown file warning."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a non-markdown file
            txt_file = Path(temp_dir) / "test.txt"
            txt_file.write_text("Not markdown")
            
            # Should return empty list and show warning
            result = find_markdown_files(txt_file)
            assert len(result) == 0
