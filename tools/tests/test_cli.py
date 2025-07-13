"""Tests for the CLI module."""
import os
import tempfile
import pytest
from click.testing import CliRunner
from tools.cli import cli, extract_command, drawio_command, version


class TestCLI:
    """Test cases for the CLI interface."""

    def setUp(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_version_command(self):
        """Test the version command."""
        runner = CliRunner()
        result = runner.invoke(version)
        
        assert result.exit_code == 0
        assert "mermaid-tools version" in result.output

    def test_help_command(self):
        """Test the help command."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        
        assert result.exit_code == 0
        assert "extract" in result.output
        assert "to-drawio" in result.output
        assert "version" in result.output

    def test_extract_help(self):
        """Test the extract command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ['extract', '--help'])
        
        assert result.exit_code == 0
        assert "Extract Mermaid diagrams" in result.output

    def test_to_drawio_help(self):
        """Test the to-drawio command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ['to-drawio', '--help'])
        
        assert result.exit_code == 0
        assert "Generate Draw.io files" in result.output

    def test_extract_with_valid_directory(self):
        """Test extract command with a valid directory containing markdown files."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test markdown file
            md_file = os.path.join(temp_dir, "test.md")
            with open(md_file, 'w') as f:
                f.write("""
# Test Document

```mermaid
graph TD
    A --> B
```
""")
            
            result = runner.invoke(cli, ['extract', temp_dir])
            
            # Should complete successfully
            assert result.exit_code == 0
            assert "Generated" in result.output or "Summary" in result.output

    def test_extract_with_nonexistent_directory(self):
        """Test extract command with non-existent directory."""
        runner = CliRunner()
        result = runner.invoke(cli, ['extract', '/nonexistent/directory'])
        
        # Should handle error gracefully
        assert result.exit_code != 0 or "not found" in result.output or "No files found" in result.output

    def test_extract_with_no_mermaid_files(self):
        """Test extract command with directory containing no mermaid diagrams."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test markdown file without mermaid diagrams
            md_file = os.path.join(temp_dir, "test.md")
            with open(md_file, 'w') as f:
                f.write("""
# Test Document

```python
print("Hello, World!")
```
""")
            
            result = runner.invoke(cli, ['extract', temp_dir])
            
            # Should complete successfully but find no diagrams
            assert result.exit_code == 0
            assert "No Mermaid diagrams found" in result.output or "found 0" in result.output

    def test_to_drawio_with_valid_directory(self):
        """Test to-drawio command with a valid directory containing mermaid files."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test mermaid file
            mmd_file = os.path.join(temp_dir, "test.mmd")
            with open(mmd_file, 'w') as f:
                f.write("graph TD\\n    A --> B")
            
            result = runner.invoke(cli, ['to-drawio', temp_dir])
            
            # Should complete successfully
            assert result.exit_code == 0
            assert "Generated" in result.output or "Created" in result.output

    def test_to_drawio_with_nonexistent_directory(self):
        """Test to-drawio command with non-existent directory."""
        runner = CliRunner()
        result = runner.invoke(cli, ['to-drawio', '/nonexistent/directory'])
        
        # Should handle error gracefully
        assert result.exit_code == 0 and "Error" in result.output

    def test_to_drawio_with_no_mermaid_files(self):
        """Test to-drawio command with directory containing no mermaid files."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test text file (not mermaid)
            txt_file = os.path.join(temp_dir, "test.txt")
            with open(txt_file, 'w') as f:
                f.write("This is not a mermaid file")
            
            result = runner.invoke(cli, ['to-drawio', temp_dir])
            
            # Should complete successfully but find no files
            assert result.exit_code == 0
            assert "No Mermaid files found" in result.output or "found 0" in result.output

    def test_extract_with_output_option(self):
        """Test extract command with output directory option."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test markdown file
            md_file = os.path.join(temp_dir, "test.md")
            with open(md_file, 'w') as f:
                f.write("""
# Test Document

```mermaid
graph TD
    A --> B
```
""")
            
            output_dir = os.path.join(temp_dir, "output")
            os.makedirs(output_dir, exist_ok=True)
            
            result = runner.invoke(cli, ['extract', temp_dir, '--output-dir', output_dir])
            
            # Should complete successfully
            assert result.exit_code == 0

    def test_extract_with_verbose_option(self):
        """Test extract command with verbose option."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test markdown file
            md_file = os.path.join(temp_dir, "test.md")
            with open(md_file, 'w') as f:
                f.write("""
# Test Document

```mermaid
graph TD
    A --> B
```
""")
            
            result = runner.invoke(cli, ['extract', temp_dir, '--verbose'])
            
            # Should complete successfully and show verbose output
            assert result.exit_code == 0
            # Verbose output should contain more details
            assert len(result.output) > 0

    def test_to_drawio_with_output_option(self):
        """Test to-drawio command with output directory option."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test mermaid file
            mmd_file = os.path.join(temp_dir, "test.mmd")
            with open(mmd_file, 'w') as f:
                f.write("graph TD\\n    A --> B")
            
            output_file = os.path.join(temp_dir, "output.drawio")
            
            result = runner.invoke(cli, ['to-drawio', temp_dir, output_file])
            
            # Should complete successfully
            assert result.exit_code == 0

    def test_cli_integration(self):
        """Test full CLI integration with both extract and to-drawio commands."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test markdown file
            md_file = os.path.join(temp_dir, "test.md")
            with open(md_file, 'w') as f:
                f.write("""
# Test Document

```mermaid
graph TD
    A --> B
```
""")
            
            # First extract mermaid diagrams
            result1 = runner.invoke(cli, ['extract', temp_dir])
            assert result1.exit_code == 0
            
            # Then convert to drawio (if any .mmd files were created)
            result2 = runner.invoke(cli, ['to-drawio', temp_dir])
            assert result2.exit_code == 0
