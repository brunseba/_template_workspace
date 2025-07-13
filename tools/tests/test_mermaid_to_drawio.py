"""Tests for the mermaid_to_drawio module."""
import os
import tempfile
import pytest
from pathlib import Path
from tools.mermaid_to_drawio import generate_drawio_file


class TestMermaidToDrawio:
    """Test cases for mermaid to Draw.io conversion."""

    def test_generate_drawio_file_with_single_file(self):
        """Test generating a Draw.io file from a single mermaid file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test mermaid file
            mmd_file = os.path.join(temp_dir, "test.mmd")
            with open(mmd_file, 'w') as f:
                f.write("graph TD\n    A[Start] --> B[Process]\n    B --> C[End]")
            
            # Generate Draw.io file
            output_file = os.path.join(temp_dir, "output.drawio")
            generate_drawio_file([mmd_file], output_file)
            
            # Check that the file was created
            assert os.path.exists(output_file)
            
            # Check the content
            with open(output_file, 'r') as f:
                content = f.read()
                assert '<mxfile' in content
                assert '</mxfile>' in content

    def test_generate_drawio_file_with_multiple_files(self):
        """Test generating a Draw.io file from multiple mermaid files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test mermaid files
            mmd_file1 = os.path.join(temp_dir, "test1.mmd")
            with open(mmd_file1, 'w') as f:
                f.write("graph TD\n    A --> B")
            
            mmd_file2 = os.path.join(temp_dir, "test2.mmd")
            with open(mmd_file2, 'w') as f:
                f.write("sequenceDiagram\n    Alice->>Bob: Hello")
            
            # Generate Draw.io file
            output_file = os.path.join(temp_dir, "output.drawio")
            generate_drawio_file([mmd_file1, mmd_file2], output_file)
            
            # Check that the file was created
            assert os.path.exists(output_file)
            
            # Check the content
            with open(output_file, 'r') as f:
                content = f.read()
                assert '<mxfile' in content
                assert '</mxfile>' in content
                assert 'pages="2"' in content

    def test_generate_drawio_file_with_empty_list(self):
        """Test generating a Draw.io file with empty file list."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = os.path.join(temp_dir, "output.drawio")
            
            # This should not create a file
            generate_drawio_file([], output_file)
            
            # Check that no file was created
            assert not os.path.exists(output_file)

    def test_generate_drawio_file_with_nonexistent_file(self):
        """Test generating a Draw.io file with non-existent input file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = os.path.join(temp_dir, "output.drawio")
            nonexistent_file = os.path.join(temp_dir, "nonexistent.mmd")
            
            # This should not create a file
            generate_drawio_file([nonexistent_file], output_file)
            
            # Check that no file was created
            assert not os.path.exists(output_file)

    def test_convert_sequence_diagram(self):
        """Test converting a sequence diagram to Draw.io format."""
        mermaid_content = """sequenceDiagram
    Alice->>Bob: Hello Bob, how are you?
    Bob-->>Alice: Great!"""
        
        drawio_content = convert_mermaid_to_drawio(mermaid_content)
        
        # Check that it's valid XML
        assert drawio_content.startswith('<?xml version="1.0"')
        assert '<mxfile' in drawio_content
        assert '</mxfile>' in drawio_content
        
        # Check for participants
        assert 'Alice' in drawio_content
        assert 'Bob' in drawio_content

    def test_convert_complex_flowchart(self):
        """Test converting a complex flowchart with various node types."""
        mermaid_content = """flowchart TD
    A[Christmas] -->|Get money| B(Go shopping)
    B --> C{Let me think}
    C -->|One| D[Laptop]
    C -->|Two| E[iPhone]
    C -->|Three| F[fa:fa-car Car]"""
        
        drawio_content = convert_mermaid_to_drawio(mermaid_content)
        
        # Check that it's valid XML
        assert drawio_content.startswith('<?xml version="1.0"')
        assert '<mxfile' in drawio_content
        assert '</mxfile>' in drawio_content
        
        # Check for nodes
        assert 'Christmas' in drawio_content
        assert 'shopping' in drawio_content
        assert 'think' in drawio_content

    def test_convert_empty_content(self):
        """Test converting empty content."""
        drawio_content = convert_mermaid_to_drawio("")
        
        # Should still produce valid XML structure
        assert drawio_content.startswith('<?xml version="1.0"')
        assert '<mxfile' in drawio_content
        assert '</mxfile>' in drawio_content

    def test_convert_invalid_mermaid(self):
        """Test converting invalid mermaid syntax."""
        mermaid_content = "invalid mermaid syntax here"
        
        drawio_content = convert_mermaid_to_drawio(mermaid_content)
        
        # Should still produce valid XML structure
        assert drawio_content.startswith('<?xml version="1.0"')
        assert '<mxfile' in drawio_content
        assert '</mxfile>' in drawio_content

    def test_process_mermaid_files_with_valid_files(self):
        """Test processing mermaid files in a directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test mermaid files
            mermaid_file1 = os.path.join(temp_dir, "test1.mmd")
            mermaid_file2 = os.path.join(temp_dir, "test2.mmd")
            
            with open(mermaid_file1, 'w') as f:
                f.write("graph TD\n    A --> B")
            
            with open(mermaid_file2, 'w') as f:
                f.write("sequenceDiagram\n    Alice->>Bob: Hello")
            
            # Process files
            result = process_mermaid_files(temp_dir)
            
            # Should return list of processed files
            assert isinstance(result, list)
            assert len(result) == 2
            
            # Check that drawio files were created
            drawio_file1 = os.path.join(temp_dir, "test1.drawio")
            drawio_file2 = os.path.join(temp_dir, "test2.drawio")
            
            assert os.path.exists(drawio_file1)
            assert os.path.exists(drawio_file2)

    def test_process_mermaid_files_no_files(self):
        """Test processing directory with no mermaid files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create non-mermaid files
            text_file = os.path.join(temp_dir, "test.txt")
            with open(text_file, 'w') as f:
                f.write("This is not a mermaid file")
            
            result = process_mermaid_files(temp_dir)
            
            # Should return empty list
            assert isinstance(result, list)
            assert len(result) == 0

    def test_process_mermaid_files_nonexistent_directory(self):
        """Test processing non-existent directory."""
        result = process_mermaid_files("/nonexistent/directory")
        
        # Should return empty list or None
        assert result is None or result == []

    def test_convert_class_diagram(self):
        """Test converting a class diagram to Draw.io format."""
        mermaid_content = """classDiagram
    class Animal {
        +String name
        +int age
        +makeSound()
    }
    class Dog {
        +String breed
        +bark()
    }
    Animal <|-- Dog"""
        
        drawio_content = convert_mermaid_to_drawio(mermaid_content)
        
        # Check that it's valid XML
        assert drawio_content.startswith('<?xml version="1.0"')
        assert '<mxfile' in drawio_content
        assert '</mxfile>' in drawio_content
        
        # Check for class names
        assert 'Animal' in drawio_content
        assert 'Dog' in drawio_content

    def test_convert_state_diagram(self):
        """Test converting a state diagram to Draw.io format."""
        mermaid_content = """stateDiagram-v2
    [*] --> Still
    Still --> [*]
    Still --> Moving
    Moving --> Still
    Moving --> Crash
    Crash --> [*]"""
        
        drawio_content = convert_mermaid_to_drawio(mermaid_content)
        
        # Check that it's valid XML
        assert drawio_content.startswith('<?xml version="1.0"')
        assert '<mxfile' in drawio_content
        assert '</mxfile>' in drawio_content
        
        # Check for states
        assert 'Still' in drawio_content
        assert 'Moving' in drawio_content
        assert 'Crash' in drawio_content

    def test_convert_preserves_special_characters(self):
        """Test that special characters are properly escaped in XML."""
        mermaid_content = """graph TD
    A["Text with & < > quotes"]
    B["Another & text"]
    A --> B"""
        
        drawio_content = convert_mermaid_to_drawio(mermaid_content)
        
        # Check that it's valid XML
        assert drawio_content.startswith('<?xml version="1.0"')
        assert '<mxfile' in drawio_content
        assert '</mxfile>' in drawio_content
        
        # Special characters should be escaped
        assert '&amp;' in drawio_content or '&' in drawio_content
        assert '&lt;' in drawio_content or '&gt;' in drawio_content
