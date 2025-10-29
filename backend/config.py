"""
Configuration module for loading environment variables and app settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ASSISTANT_NAME = os.getenv('ASSISTANT_NAME', 'Document Assistant')
ASSISTANT_INSTRUCTIONS = os.getenv('ASSISTANT_INSTRUCTIONS',
    'You are a helpful AI assistant that can analyze documents, images, and data files.')
VECTOR_STORE_NAME = os.getenv('VECTOR_STORE_NAME', '<PUT_YOUR_VECTOR_STORE_NAME_HERE>')  # <-- put your vector store name here

# Flask Configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    'png', 'jpg', 'jpeg', 'gif', 'pdf', 'bmp', 'tiff',
    'txt', 'csv', 'json', 'doc', 'docx'
}

# File type categories
IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
DOCUMENT_EXTENSIONS = {'pdf', 'txt', 'csv', 'json', 'doc', 'docx'}

# MIME types
ALLOWED_MIME_TYPES = [
    'image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/bmp', 'image/tiff',
    'application/pdf', 'text/plain', 'text/csv', 'application/json',
    'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
]
