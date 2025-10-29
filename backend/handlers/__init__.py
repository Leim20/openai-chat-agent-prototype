"""
Request handlers for different types of content (images, documents, chat).
"""
from .image_handler import handle_image_upload
from .document_handler import handle_document_upload
from .chat_handler import handle_text_message

__all__ = [
    'handle_image_upload',
    'handle_document_upload',
    'handle_text_message'
]
