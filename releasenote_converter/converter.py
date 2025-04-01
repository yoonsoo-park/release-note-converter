"""
JSON to Text converter module.

This module handles the conversion of JSON release notes to text files.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, Any, Optional


def strip_html(text: str) -> str:
    """
    Remove HTML tags from text.
    
    Args:
        text (str): HTML text to strip
        
    Returns:
        str: Plain text without HTML tags
    """
    # Simple regex to remove HTML tags
    clean_text = re.sub(r'<[^>]+>', '', text)
    # Remove extra spaces (similar to the JS version)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    return clean_text.strip()


def convert_json_to_text(
    json_file_path: str, 
    output_dir: Optional[str] = None
) -> Dict[str, str]:
    """
    Convert JSON release notes to text files.
    
    Args:
        json_file_path (str): Path to the JSON file
        output_dir (Optional[str]): Directory to save output files
            If not provided, uses './output' in the current working directory.
            
    Returns:
        Dict[str, str]: Dictionary mapping file names to their paths
    """
    # Default output directory
    if output_dir is None:
        # Use current working directory with 'output' subfolder
        output_dir = Path(os.getcwd()) / "output"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    output_files = {}
    
    # Determine the structure of the JSON data
    if isinstance(json_data, dict):
        # If it's a dictionary with keys 'Title' and 'Body__c', it's a single item
        if "Title" in json_data and "Body__c" in json_data:
            # Process as a single item
            notes_to_process = {"single_item": json_data}
        else:
            # Process as a dictionary of items
            notes_to_process = json_data
    elif isinstance(json_data, list):
        # Convert list to dictionary with indices as keys
        notes_to_process = {str(i): item for i, item in enumerate(json_data)}
    else:
        # Not a dictionary or list, unsupported format
        print(f"Warning: Unsupported JSON format. Expected a dictionary or list, got {type(json_data).__name__}")
        return output_files
    
    # Process each item in the JSON
    for key, note in notes_to_process.items():
        # Skip if note is not a dictionary
        if not isinstance(note, dict):
            print(f"Warning: Skipping item '{key}' because it is not a dictionary")
            continue
            
        # Extract title and body similar to the JS version
        if "Title" in note:
            # Convert title to filename format
            title = note["Title"].replace(" ", "_")
            title = re.sub(r'\W+', '_', title)  # Replace any non-alphanumeric with underscore
            title = re.sub(r'_+', '_', title)   # Replace multiple underscores with a single one
            title = title.strip('_')            # Remove leading/trailing underscores
        else:
            title = f"note_{key}"
        
        # Extract and clean body content
        body_field = None
        for field_name in ["Body__c", "body", "Body", "content", "Content"]:
            if field_name in note:
                body_field = field_name
                break
        
        if body_field:
            body = note[body_field]
            # Skip if body is not a string
            if not isinstance(body, str):
                print(f"Warning: Skipping item '{key}' because body is not a string")
                continue
                
            # Strip HTML and clean up
            stripped_body = strip_html(body)
            
            # Create output file path
            file_path = os.path.join(output_dir, f"{title}.txt")
            
            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(stripped_body)
            
            output_files[title] = file_path
            print(f"Created: {file_path}")
    
    return output_files