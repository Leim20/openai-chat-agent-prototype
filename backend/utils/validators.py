"""
File validation utilities.
Provides functions to validate file types, sizes, and categorize files.
"""
import config

def validate_file(filename, file_type=None, file_size=None):
    """
    Validate file based on extension, type, and size.

    Args:
        filename: Name of the file
        file_type: MIME type of the file (optional)
        file_size: Size of the file in bytes (optional)

    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    # Check if file has an extension
    if '.' not in filename:
        return False, 'File has no extension'

    # Check extension
    extension = filename.rsplit('.', 1)[1].lower()
    if extension not in config.ALLOWED_EXTENSIONS:
        return False, f'File type .{extension} not allowed. Supported types: {", ".join(config.ALLOWED_EXTENSIONS)}'

    # Check MIME type if provided
    if file_type and file_type not in config.ALLOWED_MIME_TYPES:
        # Some files might have the right extension but wrong MIME type
        # Allow if extension matches
        if extension not in config.ALLOWED_EXTENSIONS:
            return False, f'File MIME type {file_type} not allowed'

    # Check file size if provided
    if file_size and file_size > config.MAX_FILE_SIZE:
        max_size_mb = config.MAX_FILE_SIZE / (1024 * 1024)
        return False, f'File is too large. Maximum size is {max_size_mb}MB'

    return True, None


def is_image_file(filename):
    """
    Check if file is an image based on extension.

    Args:
        filename: Name of the file

    Returns:
        bool: True if file is an image, False otherwise
    """
    if '.' not in filename:
        return False

    extension = filename.rsplit('.', 1)[1].lower()
    return extension in config.IMAGE_EXTENSIONS


def is_document_file(filename):
    """
    Check if file is a document based on extension.

    Args:
        filename: Name of the file

    Returns:
        bool: True if file is a document, False otherwise
    """
    if '.' not in filename:
        return False

    extension = filename.rsplit('.', 1)[1].lower()
    return extension in config.DOCUMENT_EXTENSIONS


def get_file_category(filename):
    """
    Determine the category of a file (image or document).

    Args:
        filename: Name of the file

    Returns:
        str: 'image', 'document', or 'unknown'
    """
    if is_image_file(filename):
        return 'image'
    elif is_document_file(filename):
        return 'document'
    else:
        return 'unknown'
