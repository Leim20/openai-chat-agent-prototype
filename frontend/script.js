// Configuration
const API_BASE_URL = 'http://localhost:5000';

// Global thread ID for conversation
let currentThreadId = null;

// DOM Elements
const fileInput = document.getElementById('fileInput');
const uploadZone = document.getElementById('uploadZone');
const messagesContainer = document.getElementById('messages');
const textInput = document.getElementById('textInput');
const sendButton = document.getElementById('sendButton');

// Initialize app
async function initApp() {
    await checkBackendHealth();
    await createNewThread();
}

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

// Create a new conversation thread
async function createNewThread() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/thread`, {
            method: 'POST'
        });

        const data = await response.json();

        if (response.ok && data.success) {
            currentThreadId = data.thread_id;
            console.log('Thread created:', currentThreadId);
        } else {
            console.error('Failed to create thread:', data.error);
            addErrorMessage('Failed to initialize chat session. Please refresh.');
        }
    } catch (error) {
        console.error('Error creating thread:', error);
        addErrorMessage('Network error. Please check if the backend is running.');
    }
}

// Handle file selection
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

// Handle sending text messages
async function handleSendMessage() {
    const message = textInput.value.trim();

    if (message === '') {
        return;
    }

    if (!currentThreadId) {
        addErrorMessage('Chat session not initialized. Please refresh the page.');
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

    // Add loading message
    const loadingId = addLoadingMessage();

    try {
        // Send message to backend
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                thread_id: currentThreadId,
                message: message
            })
        });

        const data = await response.json();

        // Remove loading message
        removeMessage(loadingId);

        if (response.ok && data.success) {
            // Add AI response
            addBotTextMessage(data.response);
        } else {
            addErrorMessage(data.error || 'Failed to get response');
        }
    } catch (error) {
        removeMessage(loadingId);
        addErrorMessage('Network error. Please check if the backend is running.');
        console.error('Error:', error);
    }
}

function addBotTextMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';

    // Escape HTML but preserve newlines by converting them to <br> tags
    const escapedText = escapeHtml(text).replace(/\n/g, '<br>');

    messageDiv.innerHTML = `
        <div class="message-content">
            <p>${escapedText}</p>
        </div>
    `;
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Handle file upload and AI analysis
async function handleFile(file) {
    // Validate file size
    const maxSize = 16 * 1024 * 1024; // 16MB
    if (file.size > maxSize) {
        addErrorMessage('File is too large. Maximum size is 16MB.');
        return;
    }

    // Validate file type
    const allowedTypes = [
        'image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/bmp', 'image/tiff',
        'application/pdf', 'text/plain', 'text/csv', 'application/json',
        'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ];
    if (!allowedTypes.includes(file.type) && !file.name.match(/\.(txt|csv|json|doc|docx)$/)) {
        addErrorMessage('Invalid file type. Please upload an image, PDF, or document.');
        return;
    }

    if (!currentThreadId) {
        addErrorMessage('Chat session not initialized. Please refresh the page.');
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
        formData.append('thread_id', currentThreadId);

        // Create abort controller for timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 600000); // 10 minutes timeout

        try {
            // Send to backend with timeout
            const response = await fetch(`${API_BASE_URL}/api/upload`, {
                method: 'POST',
                body: formData,
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            const data = await response.json();

            // Remove loading message
            removeMessage(loadingId);

            if (response.ok && data.success) {
                // Add AI response
                addBotMessage(data.response, data.filename);
            } else {
                // Add error message
                addErrorMessage(data.error || 'Failed to process document');
            }
        } catch (fetchError) {
            clearTimeout(timeoutId);
            removeMessage(loadingId);

            // Check if error is due to abort (timeout)
            if (fetchError.name === 'AbortError') {
                addErrorMessage('Request timed out. The image is taking too long to process.');
            } else {
                addErrorMessage('Network error. Please check if the backend is running.');
            }
            console.error('Error:', fetchError);
        }
    } catch (error) {
        removeMessage(loadingId);
        addErrorMessage('An unexpected error occurred.');
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
            <p>📎 Uploaded: ${escapeHtml(filename)}</p>
        </div>
    `;
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function addBotMessage(text, filename) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';

    const textPreview = text.trim() || 'No response from assistant.';

    // Escape HTML but preserve newlines by converting them to <br> tags
    const escapedText = escapeHtml(textPreview).replace(/\n/g, '<br>');

    messageDiv.innerHTML = `
        <div class="message-content">
            <p class="filename">Analysis of: ${escapeHtml(filename)}</p>
            <div class="extracted-text">${escapedText}</div>
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
            <p>AI is thinking...</p>
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
        } else {
            addErrorMessage('Backend is not responding properly. Please check the server.');
        }
    } catch (error) {
        console.warn('Backend not responding. Make sure Flask server is running.');
        addErrorMessage('Cannot connect to backend. Please make sure the server is running.');
    }
}

// Initialize app on load
initApp();
