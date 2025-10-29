"""
Chat Message Handler.
Handles processing of text-only chat messages (no file attachments).

This module is specifically designed for TEXT MESSAGE processing.
"""
from services.openai_service import send_message_to_thread


def handle_text_message(thread_id, message_text):
    """
    Process a text message from the user.

    Args:
        thread_id: Thread ID for the conversation
        message_text: Text content of the user's message

    Returns:
        dict: Response containing success status and response text
              Format: {
                  'success': bool,
                  'response': str,
                  'error': str (only if success=False)
              }
    """
    # Validate input
    if not thread_id:
        return {
            'success': False,
            'error': 'thread_id is required'
        }

    if not message_text or not message_text.strip():
        return {
            'success': False,
            'error': 'message text cannot be empty'
        }

    try:
        # Send message to assistant
        response_text = send_message_to_thread(
            thread_id=thread_id,
            message_content=message_text
        )

        return {
            'success': True,
            'response': response_text
        }

    except Exception as e:
        return {
            'success': False,
            'error': f'Error processing message: {str(e)}'
        }


def validate_message_input(message_text, max_length=10000):
    """
    Validate user message input.

    Args:
        message_text: Text to validate
        max_length: Maximum allowed length

    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not message_text:
        return False, 'Message cannot be empty'

    if not message_text.strip():
        return False, 'Message cannot be only whitespace'

    if len(message_text) > max_length:
        return False, f'Message too long (max {max_length} characters)'

    return True, None
