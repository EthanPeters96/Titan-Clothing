import re
import os


def clean_filename(filename):
    """
    Clean a filename by:
    1. Converting to lowercase
    2. Removing special characters
    3. Replacing spaces with hyphens
    4. Removing multiple dots before extension
    """
    # Get the name and extension
    name, ext = os.path.splitext(filename)
    
    # Convert to lowercase
    name = name.lower()
    
    # Remove special characters
    name = re.sub(r'[^a-z0-9\s-]', '', name)
    
    # Replace spaces with hyphens
    name = re.sub(r'\s+', '-', name)
    
    # Remove multiple hyphens
    name = re.sub(r'-+', '-', name)
    
    # Remove leading/trailing hyphens
    name = name.strip('-')
    
    # Convert extension to lowercase
    ext = ext.lower()
    
    return f"{name}{ext}" 