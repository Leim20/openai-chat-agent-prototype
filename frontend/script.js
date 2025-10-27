// Configuration
const API_BASE_URL = 'http://localhost:5000';

// DOM Elements
const fileInput = document.getElementById('fileInput');
const uploadZone = document.getElementById('uploadZone');
const messagesContainer = document.getElementById('messages');
const textInput = document.getElementById('textInput');
const sendButton = document.getElementById('sendButton');

// Event Listeners
uploadZone.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', handleFileSelect);
sendButton.addEventListener('click', handleSendMessage);
textInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSendMessage();
    }
});

// Drag and drop handlers
uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.classList.add('dragover');
});

uploadZone.addEventListener('dragleave', () => {
    uploadZone.classList.remove('dragover');
});

uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

// Handle file selection
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

// Handle sending text messages
function handleSendMessage() {
    const message = textInput.value.trim();

    if (message === '') {
        return;
    }

    // Add user text message to chat
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <p>${escapeHtml(message)}</p>
        </div>
    `;
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();

    // Clear input
    textInput.value = '';

    // Optional: Add bot response (for now just echo back)
    setTimeout(() => {
        addBotTextMessage('Message received! You can upload a document to extract text.');
    }, 500);
}

function addBotTextMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <p>${escapeHtml(text)}</p>
        </div>
    `;
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Handle file upload and OCR processing
async function handleFile(file) {
    // Validate file size
    const maxSize = 16 * 1024 * 1024; // 16MB
    if (file.size > maxSize) {
        addErrorMessage('File is too large. Maximum size is 16MB.');
        return;
    }

    // Validate file type
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/bmp', 'image/tiff', 'application/pdf'];
    if (!allowedTypes.includes(file.type)) {
        addErrorMessage('Invalid file type. Please upload an image or PDF.');
        return;
    }

    // Add user message
    addUserMessage(file.name);

    // Add loading message
    const loadingId = addLoadingMessage();

    try {
        // Prepare form data
        const formData = new FormData();
        formData.append('file', file);

        // Send to backend
        const response = await fetch(`${API_BASE_URL}/api/ocr`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // Remove loading message
        removeMessage(loadingId);

        if (response.ok && data.success) {
            // Add success message with extracted text
            addBotMessage(data.text, data.filename);
        } else {
            // Add error message
            addErrorMessage(data.error || 'Failed to process document');
        }
    } catch (error) {
        removeMessage(loadingId);
        addErrorMessage('Network error. Please check if the backend is running.');
        console.error('Error:', error);
    }

    // Reset file input
    fileInput.value = '';
}

// UI Functions
function addUserMessage(filename) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <p>📎 Uploaded: ${filename}</p>
        </div>
    `;
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function addBotMessage(text, filename) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';

    const textPreview = text.trim() || 'No text found in the document.';

    messageDiv.innerHTML = `
        <div class="message-content">
            <p class="filename">Extracted from: ${filename}</p>
            <div class="extracted-text">${escapeHtml(textPreview)}</div>
        </div>
    `;
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function addLoadingMessage() {
    const messageId = 'loading-' + Date.now();
    const messageDiv = document.createElement('div');
    messageDiv.id = messageId;
    messageDiv.className = 'message bot-message';
    messageDiv.innerHTML = `
        <div class="message-content loading-message">
            <div class="spinner"></div>
            <p>Processing document...</p>
        </div>
    `;
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
    return messageId;
}

function addErrorMessage(errorText) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message error-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <p>❌ Error: ${escapeHtml(errorText)}</p>
        </div>
    `;
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function removeMessage(messageId) {
    const message = document.getElementById(messageId);
    if (message) {
        message.remove();
    }
}

function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Check backend health on load
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        if (response.ok) {
            console.log('Backend is running');
        }
    } catch (error) {
        console.warn('Backend not responding. Make sure Flask server is running.');
    }
}

checkBackendHealth();
