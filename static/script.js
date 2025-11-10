// DOM Elements
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const queryInput = document.getElementById('queryInput');
const sendBtn = document.getElementById('sendBtn');
const chatBox = document.getElementById('chatBox');
const docCount = document.getElementById('docCount');
const modelName = document.getElementById('modelName');
const clearBtn = document.getElementById('clearBtn');

// State
let isUploading = false;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    updateStatus();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    console.log('Setting up event listeners...');
    console.log('uploadBtn:', uploadBtn);
    console.log('sendBtn:', sendBtn);
    console.log('clearBtn:', clearBtn);
    console.log('queryInput:', queryInput);
    
    uploadBtn.addEventListener('click', function(e) {
        console.log('Upload button clicked, preventDefault');
        e.preventDefault();
        e.stopPropagation();
        handleUpload();
    });
    sendBtn.addEventListener('click', function(e) {
        console.log('Send button clicked, preventDefault');
        e.preventDefault();
        e.stopPropagation();
        handleQuery();
    });
    clearBtn.addEventListener('click', function(e) {
        console.log('Clear button clicked, preventDefault');
        e.preventDefault();
        e.stopPropagation();
        handleClear();
    });
    queryInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            console.log('Enter key pressed on query input, preventDefault');
            e.preventDefault();
            e.stopPropagation();
            handleQuery();
        }
    });
    console.log('Event listeners set up complete');
}

// Update status (document count and model name)
function updateStatus() {
    fetch('/status')
        .then(response => response.json())
        .then(data => {
            if (data.documents !== undefined) {
                docCount.textContent = data.documents;
            }
            if (data.model) {
                modelName.textContent = data.model;
            }
        })
        .catch(error => console.error('Error updating status:', error));
}

// Handle file upload
function handleUpload() {
    console.log('handleUpload called');
    const file = fileInput.files[0];
    console.log('Selected file:', file);
    
    if (!file) {
        console.log('No file selected');
        showMessage('Please select a PDF file', 'error');
        return;
    }
    
    if (isUploading) {
        console.log('Already uploading');
        return;
    }
    
    isUploading = true;
    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Uploading...';
    
    // Show progress bar
    const uploadSection = uploadBtn.parentElement;
    let progressBar = uploadSection.querySelector('.progress');
    if (!progressBar) {
        progressBar = document.createElement('div');
        progressBar.className = 'progress';
        progressBar.innerHTML = '<div class="progress-bar"></div>';
        uploadSection.appendChild(progressBar);
    }
    progressBar.style.display = 'block';
    progressBar.querySelector('.progress-bar').style.width = '0%';
    
    const formData = new FormData();
    formData.append('file', file);
    
    console.log('Starting file upload via fetch...');
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        console.log('Upload response status:', response.status);
        if (!response.ok) {
            throw new Error('Upload failed: HTTP ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        console.log('Upload response JSON:', data);
        progressBar.style.display = 'none';
        isUploading = false;
        uploadBtn.disabled = false;
        uploadBtn.textContent = 'Upload PDF';
        
        if (data.success) {
            showMessage('PDF uploaded successfully! Processed ' + (data.chunks || 0) + ' chunks.', 'success');
            fileInput.value = '';
            updateStatus();
        } else {
            showMessage('Error: ' + (data.message || 'Unknown error'), 'error');
        }
    })
    .catch(error => {
        console.error('Upload error:', error);
        progressBar.style.display = 'none';
        isUploading = false;
        uploadBtn.disabled = false;
        uploadBtn.textContent = 'Upload PDF';
        showMessage('Upload error: ' + error.message, 'error');
    });
}

// Handle query submission
function handleQuery() {
    console.log('handleQuery called');
    const query = queryInput.value.trim();
    console.log('Query text:', query);
    
    if (!query) {
        console.log('Query empty, returning');
        return;
    }
    
    console.log('Adding message to chat...');
    // Add user message to chat
    addMessageToChat(query, 'user');
    queryInput.value = '';
    sendBtn.disabled = true;
    console.log('Sending fetch request...');
    
    // Send query to backend
    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => {
        console.log('Fetch response received, status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Response JSON parsed:', data);
        sendBtn.disabled = false;
        
        if (data.success) {
            let assistantMessage = data.answer || 'No response';
            
            // Add sources if available
            if (data.sources && data.sources.length > 0) {
                assistantMessage += '\n\n<div class="sources"><strong>Sources:</strong>';
                data.sources.forEach(source => {
                    assistantMessage += '<div class="source-item">• ' + escapeHtml(source) + '</div>';
                });
                assistantMessage += '</div>';
            }
            
            console.log('Adding assistant message to chat');
            addMessageToChat(assistantMessage, 'assistant');
        } else {
            console.log('Response not successful:', data.message);
            addMessageToChat('Error: ' + (data.message || 'Failed to get response'), 'assistant');
        }
    })
    .catch(error => {
        sendBtn.disabled = false;
        console.error('Fetch error:', error);
        addMessageToChat('Error: Connection failed', 'assistant');
    });
}

// Add message to chat
function addMessageToChat(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + sender;
    
    // Check if content contains HTML (sources)
    if (content.includes('<div class="sources">')) {
        messageDiv.innerHTML = '<p>' + content.substring(0, content.indexOf('<div class="sources">')) + '</p>' +
                               content.substring(content.indexOf('<div class="sources">'));
    } else {
        messageDiv.innerHTML = '<p>' + escapeHtml(content) + '</p>';
    }
    
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Show status message
function showMessage(text, type) {
    const uploadSection = uploadBtn.parentElement;
    
    let messageBox = uploadSection.querySelector('.message-box');
    if (!messageBox) {
        messageBox = document.createElement('div');
        messageBox.className = 'message-box';
        uploadSection.appendChild(messageBox);
    }
    
    messageBox.textContent = text;
    messageBox.className = 'message-box ' + type;
    messageBox.style.display = 'block';
    
    // Also show in chat if it's a success message
    if (type === 'success') {
        const chatMessage = document.createElement('div');
        chatMessage.className = 'message system-message';
        chatMessage.innerHTML = '<p style="color: #28a745; font-weight: 600; text-align: center;">✓ ' + text + '</p>';
        chatBox.appendChild(chatMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        messageBox.style.display = 'none';
    }, 5000);
}

// Handle clear database
function handleClear() {
    console.log('handleClear called');
    if (!confirm('Are you sure you want to clear the database? This action cannot be undone.')) {
        console.log('Clear cancelled');
        return;
    }
    
    console.log('Sending clear request to /clear');
    fetch('/clear', {
        method: 'POST',
    })
    .then(response => {
        console.log('Clear response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Clear response data:', data);
        if (data.success) {
            console.log('Clear successful, updating UI');
            showMessage('Database cleared successfully!', 'success');
            chatBox.innerHTML = '';
            updateStatus();
        } else {
            console.log('Clear failed:', data.message);
            showMessage('Error: ' + data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Clear error:', error);
        showMessage('Error clearing database: ' + error.message, 'error');
    });
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
