# 🚀 Quick Start - Project Lexora Flask GUI

## Prerequisites

- Python 3.10+
- `.env` file with API keys set
- `requirements.txt` installed

## Quick Start (3 Steps)

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Run Flask App
```powershell
python app.py
```

### Step 3: Open in Browser
- Open: http://localhost:5000
- You should see the chat interface

---

## Using the App

### 1. Upload PDF
1. Click "Choose File" in the sidebar
2. Select a PDF document
3. Click "Upload" button
4. Wait for success message

### 2. Ask a Question
1. Type your question in the chat input
2. Press Enter or click "Send" button
3. Wait for response (first query takes 30+ seconds)

### 3. View Results
- Answer appears with sources
- Sources show which documents were used
- Ask follow-up questions

### 4. Manage Documents
- Status shows number of documents uploaded
- "Clear DB" button deletes all documents

---

## Troubleshooting Quick Links

| Issue | Check |
|-------|-------|
| Page won't load | Is `run_flask.py` running? |
| Can't upload | Is PDF file valid? Check browser console |
| No query response | Check Flask terminal for ERROR messages |
| Status shows 0 documents | Upload a PDF first |
| LLM API error | Check OPENAI_API_KEY in `.env` |

**Full troubleshooting**: See `docs/TROUBLESHOOTING.md`

---

## Debug Mode

If something goes wrong:

```powershell
# 1. Check health
python diagnostic.py

# 2. Test endpoints
python test_flask_endpoints.py

# 3. Watch Flask logs
# (Look in the terminal running run_flask.py)

# 4. Check browser console
# (Press F12 in browser)
```

---

## Performance Tips

- First query takes **30-60 seconds** (normal - LLM inference)
- Subsequent queries are faster
- Ask clear, specific questions for better results
- Larger PDFs take longer to process

---

## File Structure

```
├── app.py                    # Flask application
├── run_flask.py             # Enhanced runner with debugging
├── diagnostic.py            # System health checker
├── test_flask_endpoints.py  # Endpoint tester
├── templates/
│   └── index.html          # Web interface
├── static/
│   ├── style.css          # Styling
│   └── script.js          # Frontend logic
├── uploads/               # PDF uploads folder
├── chroma_db/            # Vector database
└── docs/
    ├── FLASK_GUI_GUIDE.md      # Full documentation
    ├── TROUBLESHOOTING.md      # Debugging guide
    └── FIXES_APPLIED.md        # What was fixed
```

---

## Common Commands

```powershell
# Start the app
python run_flask.py

# Check system health
python diagnostic.py

# Test all endpoints
python test_flask_endpoints.py

# View recent logs
Get-Content logs/app.log -Tail 50

# Clear uploads folder
Remove-Item uploads/* -Force

# Clear database
Remove-Item chroma_db -Recurse -Force
```

---

## Next Steps

1. ✅ Run `python run_flask.py`
2. ✅ Open http://localhost:5000
3. ✅ Upload a PDF
4. ✅ Ask a question
5. ✅ See answer appear

**Everything working?** → Ready for production use!

**Having issues?** → See `docs/TROUBLESHOOTING.md`

---

For detailed documentation, see:
- `docs/FLASK_GUI_GUIDE.md` - Complete API reference
- `docs/TROUBLESHOOTING.md` - Debugging guide
- `docs/FIXES_APPLIED.md` - Technical details

Enjoy! 🎉
