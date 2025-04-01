#!/usr/bin/env python3
import json
import sys
import traceback

def main():
    try:
        # The JSON file path is the first argument
        json_file_path = sys.argv[1]
        
        # Load the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # Check the structure
        print(f"Type of json_data: {type(json_data)}")
        
        if isinstance(json_data, dict):
            print(f"Keys in the dictionary: {list(json_data.keys())}")
            
            # Check for Title and Body__c
            if "Title" in json_data and "Body__c" in json_data:
                print("Found Title and Body__c in the root dictionary")
                print(f"Title: {json_data['Title']}")
                print(f"Body__c length: {len(json_data['Body__c'])}")
            else:
                # Check the first item if it's a nested structure
                first_key = list(json_data.keys())[0]
                first_item = json_data[first_key]
                print(f"Type of first item: {type(first_item)}")
                
                if isinstance(first_item, dict):
                    print(f"Keys in first item: {list(first_item.keys())}")
                else:
                    print(f"First item is not a dictionary: {first_item}")
        else:
            print(f"JSON data is not a dictionary but a {type(json_data).__name__}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()