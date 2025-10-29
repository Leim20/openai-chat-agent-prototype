# AI Document Assistant - Setup Guide

A localhost AI agent powered by OpenAI Assistant API with chat interface and file upload capabilities.

## Features

- 🤖 Chat with GPT-4 Turbo AI assistant
- 📄 Upload and analyze documents (PDF, DOCX, TXT, CSV, JSON)
- 🖼️ Analyze images (PNG, JPG, GIF, BMP, TIFF)
- 💬 Chat-style interface with conversation threads
- 🔒 Runs completely locally (data sent only to OpenAI API)

## Prerequisites

1. **Python 3.7+** - [Download Python](https://www.python.org/downloads/)
2. **OpenAI API Key** - Get one from [platform.openai.com](https://platform.openai.com/api-keys)
3. **Git** (optional) - For cloning the repository

## Quick Start

### Step 1: Install Python Dependencies

Open Command Prompt and navigate to the backend folder:

```bash
cd C:\Users\Hp\Downloads\localhost-openai-api-agent\backend
```

Create and activate a virtual environment (recommended):

```bash
python -m venv venv
venv\Scripts\activate
```

Install required packages:

```bash
pip install -r requirements.txt
```

### Step 2: Configure OpenAI API Key

1. Open `backend\.env` file in a text editor
2. Replace `your_openai_api_key_here` with your actual OpenAI API key:

```env
OPENAI_API_KEY=  # <-- put your OpenAI API key here
```

3. Save the file

**IMPORTANT:** Never share your `.env` file or commit it to version control!

### Step 3: Start the Backend Server

In the backend folder with virtual environment activated:

```bash
python app.py
```

You should see:
```
Assistant 'Document Assistant' is ready!
 * Running on http://127.0.0.1:5000
```

### Step 4: Open the Frontend

#### Option A: Direct File Access (Simplest)

1. Navigate to `frontend` folder
2. Double-click `index.html` to open in your browser

#### Option B: Using Python HTTP Server (Recommended)

Open a NEW Command Prompt window:

```bash
cd C:\Users\Hp\Downloads\localhost-openai-api-agent\frontend
python -m http.server 8080
```

Then open your browser to: http://localhost:8080

## Usage

### Text Chat

1. Type a message in the input box at the bottom
2. Press Enter or click the send button
3. Wait for the AI assistant to respond

**Example prompts:**
- "What can you help me with?"
- "Explain quantum computing in simple terms"
- "Write a Python function to calculate fibonacci numbers"

### File Upload

1. Click the upload area or drag & drop a file
2. The AI will automatically analyze the file
3. Ask follow-up questions about the uploaded file

**Supported file types:**
- Documents: PDF, DOCX, TXT
- Data: CSV, JSON
- Images: PNG, JPG, GIF, BMP, TIFF
- Max size: 16MB

**Example use cases:**
- Upload a PDF and ask "Summarize this document"
- Upload an image and ask "What's in this image?"
- Upload a CSV and ask "Analyze this data"

## Configuration

### Change AI Model

Edit `backend\app.py` line 52:

```python
model="gpt-4-turbo",  # Options: gpt-4, gpt-4-turbo, gpt-3.5-turbo
```

### Customize Assistant Instructions

Edit `backend\.env`:

```env
ASSISTANT_INSTRUCTIONS=You are a helpful assistant specialized in [your domain]. You help users by...
```

### Change Assistant Name

Edit `backend\.env`:

```env
ASSISTANT_NAME=My Custom Assistant
```

## API Endpoints

The backend provides these REST API endpoints:

- `GET /api/health` - Health check
- `POST /api/thread` - Create a new conversation thread
- `POST /api/chat` - Send a text message
  ```json
  {
    "thread_id": "thread_xxx",
    "message": "Your message here"
  }
  ```
- `POST /api/upload` - Upload a file (multipart/form-data)
  - `file`: The file to upload
  - `thread_id`: The conversation thread ID
  - `message`: Optional message about the file

## Troubleshooting

### Backend won't start

**Error: "No module named 'openai'"**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt`

**Error: "OpenAI API key not found"**
- Check that `.env` file exists in `backend` folder
- Verify your API key is correct and starts with `sk-`
- Make sure there are no quotes around the API key

### Frontend can't connect to backend

**Error: "Network error. Please check if the backend is running"**
- Verify Flask is running on http://127.0.0.1:5000
- Check Windows Firewall isn't blocking Python
- Try accessing http://localhost:5000/api/health in your browser

**CORS errors in browser console**
- Make sure you're accessing via `localhost`, not `127.0.0.1`
- Verify `flask-cors` is installed: `pip install flask-cors`

### Assistant not responding

**Timeout errors**
- Large files may take longer to process
- Default timeout is 60 seconds (configurable in app.py line 61)
- Check your internet connection (OpenAI API requires internet)

**API errors**
- Verify your OpenAI API key is valid and has credits
- Check OpenAI service status at https://status.openai.com
- Review Flask console logs for detailed error messages

### File upload fails

**"File type not allowed"**
- Check the file extension matches supported types
- Verify file is not corrupted

**"File is too large"**
- Maximum file size is 16MB
- Compress or split large files

## Project Structure

```
localhost-openai-api-agent/
├── backend/
│   ├── app.py              # Flask server with OpenAI Assistant API
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # Environment variables (API key)
│   ├── venv/              # Virtual environment (auto-created)
│   └── uploads/           # Temporary file storage (auto-created)
├── frontend/
│   ├── index.html         # Main HTML page
│   ├── style.css          # Styling
│   └── script.js          # Frontend logic
├── README.md              # Original project README
└── SETUP.md              # This file
```

## Security Notes

1. **API Key Protection**: Never commit `.env` file to Git
2. **Local Only**: This runs on localhost, not accessible from internet
3. **Data Privacy**: Files and messages are sent to OpenAI's servers
4. **Cleanup**: Uploaded files are deleted after processing

## Cost Considerations

This application uses OpenAI's paid API. Costs depend on:
- **Model**: GPT-4 Turbo is more expensive than GPT-3.5
- **Token Usage**: Longer conversations = higher costs
- **File Processing**: File search feature incurs additional charges

Check pricing at: https://openai.com/api/pricing

**Tip**: Start with `gpt-3.5-turbo` for testing to minimize costs.

## Advanced Features

### Multiple Conversation Sessions

Each time you refresh the page, a new conversation thread is created. To persist threads:
1. Store thread IDs in browser localStorage
2. Add thread selection UI
3. Modify `frontend/script.js` to resume existing threads

### Streaming Responses

For real-time token streaming (like ChatGPT):
1. Use OpenAI's streaming API
2. Implement Server-Sent Events (SSE) in Flask
3. Update frontend to handle streamed responses

### Custom Tools

OpenAI Assistants support custom functions:
1. Define functions in `app.py`
2. Add to assistant tools array
3. Handle function calls in the run loop

## Support & Documentation

- **OpenAI Assistant API Docs**: https://platform.openai.com/docs/assistants
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Issues**: Report bugs by creating an issue in this repository

## License

Free to use for personal and educational purposes.

## Credits

- Powered by OpenAI GPT-4 Turbo
- Built with Flask and vanilla JavaScript
- Original OCR template adapted for AI Assistant use
