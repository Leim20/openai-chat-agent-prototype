from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from werkzeug.utils import secure_filename
import socket

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'bmp', 'tiff'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# OCR.space API configuration
OCR_API_URL = 'https://api.ocr.space/parse/image'
OCR_API_KEY = 'K81209062288957'

# Configure requests session with better DNS handling
session = requests.Session()
session.trust_env = True  # Use system proxy settings

# Set default timeout for all requests
DEFAULT_TIMEOUT = 30

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Backend is running'})

@app.route('/api/ocr', methods=['POST'])
def process_ocr():
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400

        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Prepare request to OCR.space API
        with open(filepath, 'rb') as f:
            payload = {
                'apikey': OCR_API_KEY,
                'language': 'chs',  # Changed to Simplified Chinese (use 'cht' for Traditional Chinese, 'eng' for English)
                'isOverlayRequired': False,
                'detectOrientation': True,
                'scale': True,
                'OCREngine': 2
            }

            files_data = {
                'file': (filename, f, file.content_type)
            }

            # Call OCR.space API with timeout and better error handling
            try:
                response = session.post(
                    OCR_API_URL,
                    data=payload,
                    files=files_data,
                    timeout=DEFAULT_TIMEOUT,
                    verify=True
                )
            except requests.exceptions.ConnectionError as e:
                # Clean up uploaded file before returning error
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify({
                    'error': 'Cannot connect to OCR API. Please check your internet connection or try again later.'
                }), 503
            except requests.exceptions.Timeout:
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify({'error': 'OCR API request timed out. Please try again.'}), 504
            except Exception as e:
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify({'error': f'Network error: {str(e)}'}), 500

        # Clean up uploaded file
        os.remove(filepath)

        # Parse response
        if response.status_code == 200:
            result = response.json()

            if result.get('IsErroredOnProcessing'):
                return jsonify({
                    'error': result.get('ErrorMessage', ['Unknown error'])[0]
                }), 500

            # Extract text from response
            parsed_results = result.get('ParsedResults', [])
            if parsed_results:
                extracted_text = parsed_results[0].get('ParsedText', '')
                return jsonify({
                    'success': True,
                    'text': extracted_text,
                    'filename': filename
                })
            else:
                return jsonify({'error': 'No text found in image'}), 400
        else:
            return jsonify({'error': 'OCR API request failed'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
