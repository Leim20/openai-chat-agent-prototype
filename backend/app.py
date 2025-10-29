"""
Refactored Flask Application - Modular Architecture
Main entry point for the API server.

All business logic has been extracted into separate modules:
- config.py: Configuration and environment variables
- handlers/: Request handlers for images, documents, and chat
- services/: OpenAI API service and knowledge base management
- utils/: File validation and management utilities
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

# Import configuration
import config

# Import services
from services import get_or_create_assistant, create_thread, get_knowledge_file_ids

# Import handlers
from handlers import handle_image_upload, handle_document_upload, handle_text_message

# Import utilities
from utils.validators import get_file_category

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app, supports_credentials=True)

# Configure Flask settings
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_FILE_SIZE
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)


# ============================================================================
# FRONTEND ROUTES
# ============================================================================

@app.route('/')
def serve_frontend():
    """Serve the frontend HTML page."""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_path, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS, images) from frontend directory."""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_path, path)

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'message': 'Backend is running'})


@app.route('/api/thread', methods=['POST'])
def create_new_thread():
    """
    Create a new conversation thread with knowledge base attached.

    Returns:
        JSON response with thread_id and number of knowledge files
    """
    try:
        # Get knowledge base file IDs
        file_ids = get_knowledge_file_ids()

        # Create thread with knowledge base files
        thread_id = create_thread(knowledge_file_ids=file_ids if file_ids else None)

        return jsonify({
            'success': True,
            'thread_id': thread_id,
            'knowledge_files': len(file_ids) if file_ids else 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat', methods=['POST'])
def send_text_message():
    """
    Send a text message to the assistant.

    Expected JSON body:
        - thread_id: Thread ID
        - message: Text message content

    Returns:
        JSON response with assistant's reply
    """
    try:
        data = request.get_json()
        thread_id = data.get('thread_id')
        message = data.get('message')

        if not thread_id or not message:
            return jsonify({'error': 'thread_id and message are required'}), 400

        # Use chat handler
        result = handle_text_message(thread_id, message)

        if result['success']:
            return jsonify({
                'success': True,
                'response': result['response'],
                'thread_id': thread_id
            })
        else:
            return jsonify({'error': result['error']}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Upload a file (image or document) and send it to the assistant.

    Form data expected:
        - file: The file to upload
        - thread_id: Thread ID for the conversation
        - message: Optional message about the file

    This endpoint routes to the appropriate handler based on file type:
    - Images → image_handler
    - Documents → document_handler

    Returns:
        JSON response with analysis results
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        thread_id = request.form.get('thread_id')
        user_message = request.form.get('message', '')

        if not thread_id:
            return jsonify({'error': 'thread_id is required'}), 400

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Determine file category (image or document)
        file_category = get_file_category(file.filename)

        # Route to appropriate handler based on file type
        if file_category == 'image':
            result = handle_image_upload(file, thread_id, user_message)
        elif file_category == 'document':
            result = handle_document_upload(file, thread_id, user_message)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        # Return result from handler
        if result['success']:
            return jsonify({
                'success': True,
                'response': result['response'],
                'filename': result['filename'],
                'thread_id': thread_id
            })
        else:
            return jsonify({'error': result['error']}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# LEGACY ENDPOINT (for backward compatibility)
# ============================================================================

@app.route('/api/ocr', methods=['POST'])
def process_ocr():
    """
    Legacy OCR endpoint - redirects to new upload endpoint.
    Kept for backward compatibility with older frontend versions.
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Create a new thread for this request
        thread_id = create_thread()

        # Determine file type and route to appropriate handler
        file_category = get_file_category(file.filename)

        if file_category == 'image':
            result = handle_image_upload(
                file,
                thread_id,
                f"Please analyze and extract any important information from this file: {file.filename}"
            )
        elif file_category == 'document':
            result = handle_document_upload(
                file,
                thread_id,
                f"Please analyze and extract any important information from this file: {file.filename}"
            )
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        # Return result in legacy format
        if result['success']:
            return jsonify({
                'success': True,
                'text': result['response'],
                'filename': result['filename']
            })
        else:
            return jsonify({'error': result['error']}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == '__main__':
    # Initialize assistant on startup
    try:
        get_or_create_assistant()
        print(f"Assistant '{config.ASSISTANT_NAME}' is ready!")
    except Exception as e:
        print(f"Warning: Could not initialize assistant: {e}")

    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
