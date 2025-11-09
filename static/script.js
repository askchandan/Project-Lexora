// Project Lexora - Flask GUI JavaScript

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const queryForm = document.getElementById('queryForm');
const queryInput = document.getElementById('queryInput');
const uploadForm = document.getElementById('uploadForm');
const pdfFile = document.getElementById('pdfFile');
const uploadStatus = document.getElementById('uploadStatus');
const clearBtn = document.getElementById('clearBtn');

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    updateStatus();
    setInterval(updateStatus, 5000); // Update status every 5 seconds
});

// Query Form Submission
queryForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const query = queryInput.value.trim();
    if (!query) return;
    
    // Add user message to chat
    addMessage(query, 'user');
    queryInput.value = '';
    
    // Show loading indicator
    const loadingMsg = addMessage('🔄 Processing...', 'assistant');
    
    try {
        console.log('Sending query:', query);
        
        // Send query to backend
        const response = await fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('Response data:', data);
        
        // Remove loading message
        loadingMsg.remove();
        
        if (data.success) {
            // Add assistant response
            const content = document.createElement('div');
            
            const answer = document.createElement('p');
            answer.textContent = data.answer;
            content.appendChild(answer);
            
            // Add sources if available
            if (data.sources && data.sources.length > 0) {
                const sources = document.createElement('div');
                sources.className = 'sources';
                sources.innerHTML = '<strong>📚 Sources:</strong>';
                
                data.sources.forEach(source => {
                    const sourceItem = document.createElement('div');
                    sourceItem.className = 'source-item';
                    sourceItem.textContent = '• ' + source;
                    sources.appendChild(sourceItem);
                });
                
                content.appendChild(sources);
            }
            
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message assistant';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.appendChild(content);
            
            messageDiv.appendChild(contentDiv);
            chatMessages.appendChild(messageDiv);
        } else {
            addMessage('❌ Error: ' + data.message, 'assistant');
        }
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
    } catch (error) {
        console.error('Error details:', error);
        loadingMsg.remove();
        addMessage('❌ Error: ' + error.message, 'assistant');
    }
});

// Upload Form Submission
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const file = pdfFile.files[0];
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    console.log('Starting upload for file:', file.name);
    
    // Show uploading status
    showUploadStatus('📤 Uploading "' + file.name + '"...', 'info');
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        console.log('Upload response status:', response.status);
        const data = await response.json();
        console.log('Upload response data:', data);
        
        if (data.success) {
            const message = `✓ PDF "${data.filename}" uploaded! Added ${data.chunks} chunks.`;
            showUploadStatus(message, 'success');
            pdfFile.value = '';
            
            // Add message to chat
            addMessage(`📄 ${message}`, 'assistant');
            
            console.log('Updating status after upload...');
            
            // Wait a bit then update status
            setTimeout(() => {
                console.log('Calling updateStatus() after upload');
                updateStatus();
            }, 500);
            
            // Try updating again after another delay to be sure
            setTimeout(() => {
                console.log('Calling updateStatus() again after upload (retry)');
                updateStatus();
            }, 1500);
        } else {
            showUploadStatus('✗ Upload failed: ' + data.message, 'error');
            addMessage('❌ Upload error: ' + data.message, 'assistant');
        }
        
    } catch (error) {
        console.error('Upload error:', error);
        showUploadStatus('✗ Upload failed: ' + error.message, 'error');
        addMessage('❌ Upload error: ' + error.message, 'assistant');
    }
});

// Clear Database Button
clearBtn.addEventListener('click', async () => {
    if (!confirm('Are you sure you want to clear the database? This cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch('/clear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessage('🗑️ Database cleared successfully!', 'assistant');
            updateStatus();
        } else {
            addMessage('❌ Error: ' + data.message, 'assistant');
        }
        
    } catch (error) {
        addMessage('❌ Error clearing database', 'assistant');
        console.error('Error:', error);
    }
});

// Helper Functions
function addMessage(text, role) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const p = document.createElement('p');
    p.textContent = text;
    
    contentDiv.appendChild(p);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return messageDiv;
}

function showUploadStatus(message, type) {
    uploadStatus.textContent = message;
    uploadStatus.className = 'status-message ' + type;
    
    if (type === 'success') {
        setTimeout(() => {
            uploadStatus.textContent = '';
            uploadStatus.className = 'status-message';
        }, 3000);
    }
}

async function updateStatus() {
    try {
        console.log('Fetching status...');
        const response = await fetch('/status');
        console.log('Status response code:', response.status);
        
        if (!response.ok) {
            throw new Error(`Status endpoint failed: HTTP ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Status data:', data);
        
        if (data.success || data.documents !== undefined) {
            // Update even if there's an error, just show what we have
            document.getElementById('doc-count').innerHTML = 
                `Documents: <span>${data.documents || 0}</span>`;
            
            const modelName = data.model === 'N/A' ? 'Not configured' : data.model;
            document.getElementById('model-name').textContent = 
                data.error ? `Model: Error - ${data.error}` : `Model: ${modelName}`;
            
            console.log(`✓ Status updated: ${data.documents || 0} docs`);
        } else {
            console.error('Status endpoint returned error:', data.message);
            document.getElementById('model-name').textContent = 
                `Model: Error - ${data.message}`;
        }
    } catch (error) {
        console.error('Error updating status:', error);
        document.getElementById('model-name').textContent = 
            `Model: Error (${error.message})`;
    }
}

// Allow pressing Enter to send message
queryInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        queryForm.dispatchEvent(new Event('submit'));
    }
});
