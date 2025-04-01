"""
Command-line interface for the Release Note Converter.

This module provides a CLI for converting JSON release notes to text files.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional, List

from releasenote_converter.converter import convert_json_to_text


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Args:
        args (Optional[List[str]]): Command-line arguments to parse.
            If None, sys.argv[1:] is used.
            
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        prog="releasenote-converter",
        description="Convert JSON release notes to text files"
    )
    
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to the JSON input file"
    )
    
    parser.add_argument(
        "-o", "--output",
        required=False,
        help="Directory to save output files (optional)"
    )
    
    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the command-line application.
    
    Args:
        args (Optional[List[str]]): Command-line arguments
        
    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    try:
        parsed_args = parse_args(args)
        
        # Validate input file exists
        if not os.path.isfile(parsed_args.input):
            print(f"Error: Input file '{parsed_args.input}' does not exist.")
            return 1
        
        # Convert the JSON file to text files
        output_files = convert_json_to_text(
            parsed_args.input, 
            parsed_args.output
        )
        
        if not output_files:
            print("Warning: No release notes were found or converted.")
            return 0
            
        print(f"Successfully converted {len(output_files)} release notes to text files.")
        return 0
        
    except Exception as e:
        import traceback
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())