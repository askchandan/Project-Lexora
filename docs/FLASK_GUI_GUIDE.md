# 🚀 Project Lexora - Flask Web GUI

## Overview

A modern Flask-based web interface for the Project Lexora RAG + LLM Chatbot. Upload PDF documents and ask questions with instant answers powered by RAG and LLM.

---

## ✨ Features

- 📤 **PDF Upload**: Upload multiple PDF documents
- 💬 **Chat Interface**: Ask questions and get AI-powered answers
- 🔗 **Source Attribution**: See which documents were used
- 📊 **Document Status**: View number of indexed documents
- 🗑️ **Clear Database**: Reset all documents and start fresh
- 🎨 **Modern UI**: Clean, responsive design

---

## 📋 Installation

### 1. Install Dependencies

```powershell
pip install flask werkzeug
pip install -r requirements.txt
```

### 2. Verify Setup

```powershell
# Check Flask is installed
python -c "import flask; print('Flask:', flask.__version__)"

# Check other dependencies
python -c "from src.core.query_engine import QueryEngine; print('✓ RAG ready')"
```

---

## 🎯 Running the Application

### Start the Flask Server

```powershell
cd "c:\Users\Chandan Malakar\Desktop\PDF AI Chat"
python app.py
```

**Output should show:**
```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
```

### Access the GUI

Open your browser and go to:
```
http://localhost:5000
```

---

## 📖 How to Use

### 1. **Upload PDFs**
- Click "Choose File" in the sidebar
- Select a PDF from your computer
- Click "Upload" button
- Wait for confirmation message

### 2. **Ask Questions**
- Type your question in the chat input
- Press Enter or click "Send"
- Get instant answers with sources

### 3. **View Status**
- See document count in sidebar
- Check model being used
- Monitor upload progress

### 4. **Clear Database**
- Click "Clear DB" button
- Confirm deletion
- Database will be reset

---

## 🏗️ Project Structure

```
├── app.py                 # Flask application main file
├── templates/
│   └── index.html        # Web interface HTML
├── static/
│   ├── style.css        # Styling
│   └── script.js        # Frontend JavaScript
├── uploads/             # Uploaded PDF files
└── logs/                # Application logs
```

---

## 🔌 API Endpoints

### `GET /`
**Home page** - Loads the web interface
- Returns: HTML page

### `POST /upload`
**Upload PDF document**
- Parameters: 
  - `file`: PDF file (multipart/form-data)
- Returns:
  ```json
  {
    "success": true,
    "message": "PDF uploaded successfully",
    "filename": "document.pdf",
    "chunks": 45
  }
  ```

### `POST /query`
**Execute query**
- Parameters:
  ```json
  {
    "query": "What is hacking?"
  }
  ```
- Returns:
  ```json
  {
    "success": true,
    "answer": "According to Section 66...",
    "sources": ["file.pdf:0:1", "file.pdf:1:2"],
    "query": "What is hacking?"
  }
  ```

### `GET /status`
**Get application status**
- Returns:
  ```json
  {
    "success": true,
    "initialized": true,
    "documents": 108,
    "model": "mistralai/mistral-7b-instruct"
  }
  ```

### `POST /clear`
**Clear database**
- Returns:
  ```json
  {
    "success": true,
    "message": "Database cleared successfully"
  }
  ```

---

## ⚙️ Configuration

Edit `.env` file to customize:

```env
# LLM Model
MODEL_NAME=mistralai/mistral-7b-instruct
TEMPERATURE=0.7
MAX_TOKENS=500

# Data paths
DATA_PATH=data
CHROMA_PATH=chroma_db

# API Keys
OPENAI_API_KEY=sk-...
OPENAI_API_BASE=https://openrouter.ai/api/v1
```

---

## 🎨 UI Features

### Sidebar
- Logo and branding
- Document count display
- Model information
- PDF upload section
- Clear database button
- Usage tips

### Chat Area
- Message history
- User and assistant messages
- Source attribution
- Real-time message updates
- Auto-scrolling

### Styling
- Modern gradient background
- Responsive design
- Smooth animations
- Professional color scheme

---

## 🐛 Troubleshooting

### Issue: Port 5000 already in use
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process
taskkill /PID <PID> /F

# Or change port in app.py (line ~165)
app.run(port=5001)
```

### Issue: PDF upload fails
- Check file size (max 50MB)
- Ensure PDF is valid
- Check `uploads/` directory permissions

### Issue: Query returns empty
- Verify PDFs are uploaded
- Check document count in status
- Try uploading a PDF first

### Issue: Flask not found
```powershell
pip install flask werkzeug
python -m pip install --upgrade pip
```

---

## 📊 Performance Tips

1. **Use smaller PDFs** - Split large documents
2. **Limit documents** - Keep indexed documents reasonable
3. **Cache responses** - Frontend caches similar queries
4. **Async uploads** - Large files upload in background

---

## 🔐 Security Notes

- ✅ API keys stored in `.env` (not committed)
- ✅ File uploads sanitized
- ✅ 50MB file size limit
- ✅ CORS not enabled (local only)
- ⚠️ Not recommended for public deployment without additional security

---

## 📈 Deployment

### Local Development
```powershell
python app.py  # Default: debug=True
```

### Production (Simple)
```python
# In app.py, change:
app.run(debug=False, host='0.0.0.0', port=5000)
```

### Using Gunicorn (Recommended)
```powershell
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📚 Related Files

- `src/core/query_engine.py` - Query processing
- `src/core/rag_pipeline.py` - Document indexing
- `src/database/chroma_manager.py` - Vector database
- `scripts/populate_database.py` - CLI version

---

## 🎓 Learning Resources

- Flask Documentation: https://flask.palletsprojects.com/
- LangChain: https://python.langchain.com/
- Chroma: https://www.trychroma.com/

---

## 📝 Commit Message

```bash
git add app.py templates/ static/ requirements.txt
git commit -m "feat: add flask web gui with pdf upload and chat"
git push origin main
```

---

**Happy Chatting!** 🚀

For issues or improvements, open an issue on GitHub.
