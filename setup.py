"""
Setup script for the releasenote-converter package.
"""

from setuptools import setup, find_packages
import os

# Read the contents of the README file
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "Release Note Converter - Convert JSON release notes to text files"

setup(
    name="releasenote-converter",
    version="0.1.0",
    description="Convert JSON release notes to text files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yoonsoo Park",
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "releasenote-converter=releasenote_converter.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)