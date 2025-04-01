"""
Tests for the CLI module.
"""

import json
import os
import tempfile
from pathlib import Path

import pytest

from releasenote_converter.cli import main, parse_args


def test_parse_args():
    """Test argument parsing."""
    # Test with required input only
    args = parse_args(["-i", "input.json"])
    assert args.input == "input.json"
    assert args.output is None
    
    # Test with both input and output
    args = parse_args(["-i", "input.json", "-o", "output_dir"])
    assert args.input == "input.json"
    assert args.output == "output_dir"
    
    # Test with long form arguments
    args = parse_args(["--input", "input.json", "--output", "output_dir"])
    assert args.input == "input.json"
    assert args.output == "output_dir"


def test_main_success():
    """Test successful execution of the main function."""
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a sample JSON file
        json_path = Path(temp_dir) / "test_cli.json"
        test_data = {
            "note1": {
                "Title": "CLI Test Note",
                "Body__c": "<p>Testing the CLI</p>"
            }
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        # Create an output directory
        output_dir = Path(temp_dir) / "cli_output"
        
        # Run the CLI
        exit_code = main(["-i", str(json_path), "-o", str(output_dir)])
        
        # Check that it succeeded
        assert exit_code == 0
        
        # Check that the expected file was created
        output_file = output_dir / "CLI_Test_Note.txt"
        assert output_file.exists()
        
        # Check the content
        with open(output_file, 'r', encoding='utf-8') as f:
            assert f.read() == "Testing the CLI"


def test_main_nonexistent_input():
    """Test error handling for nonexistent input file."""
    # Run with a non-existent file
    exit_code = main(["-i", "nonexistent_file.json"])
    
    # Should return an error code
    assert exit_code == 1


def test_main_empty_json():
    """Test handling of empty JSON file."""
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create an empty JSON file
        json_path = Path(temp_dir) / "empty.json"
        
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write("{}")
        
        # Run the CLI
        exit_code = main(["-i", str(json_path)])
        
        # Should succeed but with a warning
        assert exit_code == 0