# Local OCR Web Application

A local web application for OCR (Optical Character Recognition) with a chat-style interface. Upload documents and extract text instantly using OCR.space API.

## Features

- 📄 Upload images (PNG, JPG, GIF, BMP, TIFF) or PDFs
- 💬 Chat-style interface for easy interaction
- 🚀 Fast OCR processing using OCR.space API
- 🎨 Modern, responsive UI
- 🔒 Local deployment with nginx

## Project Structure

```
local-ocr-web/
├── backend/
│   ├── app.py              # Flask backend server
│   ├── requirements.txt    # Python dependencies
│   └── uploads/           # Temporary upload folder (auto-created)
├── frontend/
│   ├── index.html         # Main HTML page
│   ├── style.css          # Styling
│   └── script.js          # JavaScript logic
├── nginx/
│   └── nginx.conf         # nginx configuration
└── README.md
```

## Prerequisites

- Python 3.7 or higher
- nginx for Windows
- OCR.space API key (already configured: K81209062288957)

## Installation & Setup

### Step 1: Install Python Dependencies

Open Command Prompt and navigate to the backend folder:

```bash
cd C:\Users\Hp\Downloads\local-ocr-web\backend
```

Create a virtual environment (recommended):

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Step 2: Install nginx

1. Download nginx for Windows from: https://nginx.org/en/download.html
2. Extract to a location like `C:\nginx`

### Step 3: Configure nginx

Copy the nginx configuration:

1. Open `C:\nginx\conf\nginx.conf`
2. Replace its contents with the content from `nginx\nginx.conf` in this project
3. Make sure the paths in the config match your setup

## Running the Application

### Method 1: Using nginx (Recommended)

1. **Start the Flask Backend:**

Open Command Prompt in the backend folder:

```bash
cd C:\Users\Hp\Downloads\local-ocr-web\backend
venv\Scripts\activate
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

2. **Start nginx:**

Open another Command Prompt:

```bash
cd C:\nginx
nginx.exe
```

3. **Access the Application:**

Open your browser and go to:
```
http://localhost:8080
```

### Method 2: Direct Access (Without nginx)

If you want to test without nginx:

1. Start the Flask backend (same as above)
2. Open `frontend/index.html` directly in your browser
3. Or use Python's HTTP server:

```bash
cd C:\Users\Hp\Downloads\local-ocr-web\frontend
python -m http.server 8080
```

Then access: `http://localhost:8080`

**Note:** If not using nginx, you may need to update `API_BASE_URL` in `frontend/script.js`

## Usage

1. Open the application in your browser
2. Click the upload area or drag & drop a document
3. Wait for OCR processing (usually 2-5 seconds)
4. View extracted text in the chat interface
5. Upload more documents as needed

## Supported File Types

- Images: PNG, JPG, JPEG, GIF, BMP, TIFF
- Documents: PDF
- Max file size: 16MB

## Troubleshooting

### Backend not responding

- Check if Flask is running on port 5000
- Look for errors in the Command Prompt where Flask is running
- Verify Python dependencies are installed

### nginx errors

- Check if port 8080 is available
- Stop nginx: `nginx.exe -s stop`
- Reload config: `nginx.exe -s reload`
- Check nginx error logs in `C:\nginx\logs\error.log`

### CORS errors

- Make sure you're accessing via `localhost` not `127.0.0.1`
- Verify flask-cors is installed
- Check browser console for specific errors

### OCR not working

- Verify API key is correct in `backend/app.py`
- Check your internet connection (OCR.space API is online)
- Review Flask logs for API response errors

## Stopping the Application

1. **Stop Flask:** Press `Ctrl+C` in the Flask Command Prompt
2. **Stop nginx:**
```bash
cd C:\nginx
nginx.exe -s stop
```

## Configuration

### Change OCR API Key

Edit `backend/app.py` line 16:

```python
OCR_API_KEY = 'YOUR_NEW_API_KEY'
```

### Change Ports

- **Backend:** Edit `app.py` line 80 to change from port 5000
- **Frontend:** Edit `nginx/nginx.conf` line 17 to change from port 8080

### OCR Language

Edit `backend/app.py` line 49 to change language:

```python
'language': 'eng',  # Change to 'spa', 'fra', 'deu', etc.
```

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/ocr` - Upload and process document

## License

Free to use for personal and educational purposes.

## Credits

- OCR powered by OCR.space API
- Frontend design inspired by modern chat interfaces
