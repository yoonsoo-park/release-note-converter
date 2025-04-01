"""
Tests for the converter module.
"""

import json
import os
import tempfile
from pathlib import Path

import pytest

from releasenote_converter.converter import convert_json_to_text, strip_html


def test_strip_html():
    """Test the strip_html function with various HTML inputs."""
    # Test basic HTML stripping
    assert strip_html("<p>Test</p>") == "Test"
    
    # Test nested HTML
    assert strip_html("<div><p>Test <strong>bold</strong></p></div>") == "Test bold"
    
    # Test with extra spaces
    assert strip_html("<p>Test    with   spaces</p>") == "Test with spaces"


def test_convert_json_to_text():
    """Test the convert_json_to_text function with a sample JSON file."""
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a sample JSON file
        json_path = Path(temp_dir) / "test_notes.json"
        test_data = {
            "note1": {
                "Title": "Test Note 1",
                "Body__c": "<p>This is a test note</p>"
            },
            "note2": {
                "Title": "Test Note 2",
                "Body__c": "<div>This is <strong>another</strong> test note</div>"
            }
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        # Create an output directory
        output_dir = Path(temp_dir) / "output"
        
        # Run the conversion
        result = convert_json_to_text(str(json_path), str(output_dir))
        
        # Check that we have the expected output files
        assert len(result) == 2
        assert "Test_Note_1" in result
        assert "Test_Note_2" in result
        
        # Check the content of the files
        with open(result["Test_Note_1"], 'r', encoding='utf-8') as f:
            assert f.read() == "This is a test note"
            
        with open(result["Test_Note_2"], 'r', encoding='utf-8') as f:
            assert f.read() == "This is another test note"


def test_convert_json_to_text_default_output():
    """Test conversion with default output directory."""
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a sample JSON file
        json_path = Path(temp_dir) / "test_notes.json"
        test_data = {
            "note1": {
                "Title": "Test Default Output",
                "Body__c": "<p>Testing default output path</p>"
            }
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        # Create an output directory manually
        output_dir = Path(temp_dir) / "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Run the conversion with a custom output dir
        result = convert_json_to_text(str(json_path), str(output_dir))
        
        # Check the file exists
        assert "Test_Default_Output" in result
        assert os.path.isfile(result["Test_Default_Output"])
        
        # Check content
        with open(result["Test_Default_Output"], 'r', encoding='utf-8') as f:
            assert f.read() == "Testing default output path"


def test_convert_json_with_missing_fields():
    """Test handling of JSON data with missing fields."""
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a sample JSON file with missing fields
        json_path = Path(temp_dir) / "test_missing.json"
        test_data = {
            "note1": {
                # Missing Title
                "Body__c": "<p>Body without title</p>"
            },
            "note2": {
                "Title": "No Body"
                # Missing Body
            },
            "note3": {
                # Different field names
                "title": "Different Case",
                "body": "<p>Different field name</p>"
            }
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        # Create an output directory
        output_dir = Path(temp_dir) / "output"
        
        # Run the conversion
        result = convert_json_to_text(str(json_path), str(output_dir))
        
        # Should get results for note1 and note3
        assert len(result) == 2
        assert "note_note1" in result
        assert "note_note3" in result
        
        # Check content
        with open(result["note_note1"], 'r', encoding='utf-8') as f:
            assert f.read() == "Body without title"