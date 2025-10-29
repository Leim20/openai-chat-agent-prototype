"""
Document Upload Handler.
Handles processing of document files (PDF, TXT, DOCX, CSV, JSON) using file_search tool.

This module is specifically designed for DOCUMENT processing and can be:
- Easily duplicated for other projects
- Modified independently from image handling
- Tested separately from other components
"""
from utils.validators import validate_file, is_document_file
from utils.file_manager import save_temp_file, cleanup_temp_file
from services.openai_service import upload_file_to_openai, send_message_to_thread


def handle_document_upload(file, thread_id, user_message=''):
    """
    Process an uploaded document file using file_search tool.

    Args:
        file: FileStorage object from Flask request
        thread_id: Thread ID for the conversation
        user_message: Optional message from user about the document

    Returns:
        dict: Response containing success status, response text, and filename
              Format: {
                  'success': bool,
                  'response': str,
                  'filename': str,
                  'error': str (only if success=False)
              }
    """
    # Validate that it's actually a document
    if not is_document_file(file.filename):
        return {
            'success': False,
            'error': 'File is not a supported document format'
        }

    # Validate file
    is_valid, error_msg = validate_file(
        filename=file.filename,
        file_type=file.content_type,
        file_size=file.content_length
    )

    if not is_valid:
        return {
            'success': False,
            'error': error_msg
        }

    # Save file temporarily
    filepath, filename = save_temp_file(file)
    if not filepath:
        return {
            'success': False,
            'error': 'Failed to save document file'
        }

    try:
        # Upload document to OpenAI
        file_id = upload_file_to_openai(filepath)

        # Prepare message content for document analysis
        if user_message:
            message_content = f"{user_message}\n\n[File attached: {filename}]"
        else:
            message_content = f"Please analyze this file: {filename}"

        # Send to assistant with document attached (use_file_search=True for documents)
        response_text = send_message_to_thread(
            thread_id=thread_id,
            message_content=message_content,
            file_id=file_id,
            use_file_search=True  # Documents use file_search tool for text extraction
        )

        return {
            'success': True,
            'response': response_text,
            'filename': filename
        }

    except Exception as e:
        return {
            'success': False,
            'error': f'Error processing document: {str(e)}'
        }

    finally:
        # Always cleanup temporary file
        cleanup_temp_file(filepath)


def validate_document_file(filename, file_type=None, file_size=None):
    """
    Validate that a file is an acceptable document.

    Args:
        filename: Name of the file
        file_type: MIME type (optional)
        file_size: Size in bytes (optional)

    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    # Check if it's a document
    if not is_document_file(filename):
        return False, 'File is not a document'

    # Use general file validation
    return validate_file(filename, file_type, file_size)


# Additional document-specific utilities can be added here
def get_supported_document_formats():
    """
    Get list of supported document file extensions.

    Returns:
        list: List of supported extensions (without dots)
    """
    return ['pdf', 'txt', 'csv', 'json', 'doc', 'docx']


def get_document_type(filename):
    """
    Determine the specific type of document.

    Args:
        filename: Name of the file

    Returns:
        str: Document type ('pdf', 'text', 'spreadsheet', 'json', 'word', 'unknown')
    """
    if '.' not in filename:
        return 'unknown'

    extension = filename.rsplit('.', 1)[1].lower()

    type_mapping = {
        'pdf': 'pdf',
        'txt': 'text',
        'csv': 'spreadsheet',
        'json': 'json',
        'doc': 'word',
        'docx': 'word'
    }

    return type_mapping.get(extension, 'unknown')


def is_large_document(file_size_bytes):
    """
    Check if a document is considered large (>10MB).

    Args:
        file_size_bytes: Size of the file in bytes

    Returns:
        bool: True if document is large
    """
    return file_size_bytes > 10 * 1024 * 1024
