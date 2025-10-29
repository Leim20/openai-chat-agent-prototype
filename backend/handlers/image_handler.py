"""
Image Upload Handler.
Handles processing of image files using GPT-4o vision capability.

This module is specifically designed for IMAGE processing and can be:
- Easily duplicated for other projects
- Modified independently from document handling
- Tested separately from other components
"""
from utils.validators import validate_file, is_image_file
from utils.file_manager import save_temp_file, cleanup_temp_file
from services.openai_service import upload_file_to_openai, send_message_to_thread


def handle_image_upload(file, thread_id, user_message=''):
    """
    Process an uploaded image file using GPT-4o vision.

    Args:
        file: FileStorage object from Flask request
        thread_id: Thread ID for the conversation
        user_message: Optional message from user about the image

    Returns:
        dict: Response containing success status, response text, and filename
              Format: {
                  'success': bool,
                  'response': str,
                  'filename': str,
                  'error': str (only if success=False)
              }
    """
    # Validate that it's actually an image
    if not is_image_file(file.filename):
        return {
            'success': False,
            'error': 'File is not a supported image format'
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
            'error': 'Failed to save image file'
        }

    try:
        # Upload image to OpenAI with 'vision' purpose (critical for image processing)
        print(f"[DEBUG] Uploading image {filename} to OpenAI...")
        file_id = upload_file_to_openai(filepath, purpose='vision')
        print(f"[DEBUG] Image uploaded successfully. File ID: {file_id}")

        # Prepare message content for image analysis
        if user_message:
            message_content = f"{user_message}\n\n[Image attached: {filename}]"
        else:
            message_content = f"Please analyze this image: {filename}"

        print(f"[DEBUG] Sending image to thread {thread_id}...")
        # Send to assistant with image attached (use_file_search=False for vision)
        response_text = send_message_to_thread(
            thread_id=thread_id,
            message_content=message_content,
            file_id=file_id,
            use_file_search=False  # Images use GPT-4o vision, not file_search
        )
        print(f"[DEBUG] Received response from assistant")

        return {
            'success': True,
            'response': response_text,
            'filename': filename
        }

    except Exception as e:
        return {
            'success': False,
            'error': f'Error processing image: {str(e)}'
        }

    finally:
        # Always cleanup temporary file
        cleanup_temp_file(filepath)


def validate_image_file(filename, file_type=None, file_size=None):
    """
    Validate that a file is an acceptable image.

    Args:
        filename: Name of the file
        file_type: MIME type (optional)
        file_size: Size in bytes (optional)

    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    # Check if it's an image
    if not is_image_file(filename):
        return False, 'File is not an image'

    # Use general file validation
    return validate_file(filename, file_type, file_size)


# Additional image-specific utilities can be added here
def get_supported_image_formats():
    """
    Get list of supported image file extensions.

    Returns:
        list: List of supported extensions (without dots)
    """
    return ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']


def is_large_image(file_size_bytes):
    """
    Check if an image is considered large (>5MB).

    Args:
        file_size_bytes: Size of the file in bytes

    Returns:
        bool: True if image is large
    """
    return file_size_bytes > 5 * 1024 * 1024
