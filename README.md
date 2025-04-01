# Release Note Converter

A command-line tool to convert JSON release notes to text files.

## Installation

You can install the package from the local directory:

```bash
# Install in development mode
pip install -e .

# Or install normally
pip install .
```

## Usage

Once installed, you can use the command-line tool from anywhere:

```bash
# Basic usage
releasenote-converter -i path/to/your/file.json

# Specify output directory
releasenote-converter -i path/to/your/file.json -o path/to/output/directory
```

### Options

- `-i, --input`: Path to the JSON input file (required)
- `-o, --output`: Directory to save output files (optional, defaults to the 'output' directory in the project)

## Example

```bash
# Convert the sample file
releasenote-converter -i releaseNotes.json

# Specify a custom output directory
releasenote-converter -i 2024-release-notes.json -o ~/Documents/release-notes
```

## Development

### Requirements

- Python 3.6+

### Testing

Run tests using pytest:

```bash
pytest
```