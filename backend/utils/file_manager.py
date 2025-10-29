"""
File management utilities.
Provides functions for saving and cleaning up temporary files.
"""
import os
from werkzeug.utils import secure_filename
import config

def save_temp_file(file, upload_folder=None):
    """
    Save an uploaded file to a temporary location.

    Args:
        file: FileStorage object from Flask request
        upload_folder: Directory to save file (defaults to config.UPLOAD_FOLDER)

    Returns:
        tuple: (filepath: str, filename: str) or (None, None) if error
    """
    if not upload_folder:
        upload_folder = config.UPLOAD_FOLDER

    # Ensure upload folder exists
    os.makedirs(upload_folder, exist_ok=True)

    # Secure the filename
    filename = secure_filename(file.filename)

    if not filename:
        return None, None

    # Full path
    filepath = os.path.join(upload_folder, filename)

    try:
        file.save(filepath)
        return filepath, filename
    except Exception as e:
        print(f"Error saving file: {e}")
        return None, None


def cleanup_temp_file(filepath):
    """
    Delete a temporary file.

    Args:
        filepath: Path to the file to delete

    Returns:
        bool: True if deleted successfully, False otherwise
    """
    if not filepath or not os.path.exists(filepath):
        return False

    try:
        os.remove(filepath)
        return True
    except Exception as e:
        print(f"Error cleaning up file {filepath}: {e}")
        return False


def ensure_directory_exists(directory):
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        directory: Path to the directory

    Returns:
        bool: True if directory exists or was created
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {directory}: {e}")
        return False
