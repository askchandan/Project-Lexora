# Project Lexora - RAG + LLM Chatbot

**An Intelligent PDF Analysis and Chat System powered by LLM + RAG**

A production-ready Retrieval-Augmented Generation (RAG) system with a Flask web interface.

## Features

✅ **Web Interface** - Interactive Flask-based chat UI  
✅ **Document Upload** - Easy PDF upload and processing  
✅ **Real-time Chat** - Ask questions and get AI responses  
✅ **Semantic Search** - Vector similarity matching  
✅ **Source Tracking** - Shows document sources  
✅ **Database Management** - Clear and manage documents  
✅ **Docker Ready** - Production deployment  
✅ **Modular Architecture** - Clean, extensible codebase  

## Quick Start (Local)

### 1. Clone Repository
```bash
git clone https://github.com/askchandan/Project-Lexora.git
cd Project-Lexora
```

### 2. Setup Environment
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure .env
```env
OPENAI_API_KEY=your_api_key
OPENAI_API_BASE=https://openrouter.ai/api/v1
DATA_PATH=data
CHROMA_PATH=chroma_db
MODEL_NAME=mistralai/mistral-7b-instruct
```

### 4. Run
```bash
python app.py
```
Visit `http://localhost:5000`

## Docker Deployment

### Option 1: Docker Run
```bash
docker build -t project-lexora .
docker run -p 5000:5000 \
  -e OPENAI_API_KEY=your_key \
  -e OPENAI_API_BASE=https://openrouter.ai/api/v1 \
  -v lexora_data:/app/chroma_db \
  project-lexora
```

### Option 2: Docker Compose (Recommended)
```bash
# Update .env with your API key
docker-compose up -d
docker-compose logs -f
docker-compose down
```

Visit `http://localhost:5000`

## Usage Guide

### Upload PDF
1. Click "Upload PDF" button
2. Select PDF file
3. Click "Upload"
4. Wait for success message

### Ask Questions
1. Type question in input box
2. Click "Send" or press Enter
3. View AI response with sources

### Clear Database
1. Click "Clear Database"
2. Confirm action
3. Database resets

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web interface |
| GET | `/status` | System status |
| POST | `/upload` | Upload PDF |
| POST | `/query` | Ask question |
| POST | `/clear` | Clear database |

## Project Structure

```
project-lexora/
├── app.py                  # Flask application
├── requirements.txt        # Dependencies
├── Dockerfile             # Docker image
├── docker-compose.yml     # Compose config
├── .env.example          # Env template
├── README.md             # This file
├── LICENSE               # MIT License
│
├── src/
│   ├── core/             # RAG pipeline
│   ├── models/           # LLM & Embeddings
│   ├── database/         # Vector store
│   └── utils/            # Config & logging
│
├── templates/
│   └── index.html        # Web UI
│
├── static/
│   ├── script.js         # Frontend logic
│   └── style.css         # Styling
│
├── data/                 # PDF storage
└── chroma_db/           # Vector database
```

## Configuration

### Environment Variables
```env
# Required
OPENAI_API_KEY=sk_...
OPENAI_API_BASE=https://openrouter.ai/api/v1

# Optional
DATA_PATH=data
CHROMA_PATH=chroma_db
MODEL_NAME=mistralai/mistral-7b-instruct
TEMPERATURE=0.7
MAX_TOKENS=500
```

### Supported Models
- `mistralai/mistral-7b-instruct` (default)
- `gpt-3.5-turbo`
- `gpt-4`
- Other OpenRouter models

## System Requirements

**Local**
- Python 3.8+
- 2GB RAM
- 500MB disk

**Docker**
- Docker 20.10+
- Docker Compose 1.29+
- 2GB RAM
- 500MB disk

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No documents | Upload PDFs via UI |
| API error | Check .env with valid key |
| Port in use | Use different port |
| Slow response | Check API rate limits |

## Performance

- PDF Processing: ~100ms per document
- Query Response: 2-5 seconds
- Search Speed: <50ms

## Security

✅ API keys in .env (gitignored)  
✅ Input validation  
✅ Secure storage  
✅ CSRF protection ready  

## Technologies

- **Backend**: Flask, LangChain, Chroma
- **Frontend**: HTML5, CSS3, JavaScript
- **DevOps**: Docker, Docker Compose
- **AI**: Mistral-7B via OpenRouter

## Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Submit pull request

## License

MIT License - see LICENSE file

## Author

**Chandan Malakar**  
GitHub: [@askchandan](https://github.com/askchandan)

---

**Project Lexora** - Intelligent RAG Chatbot  
Powered by LangChain, Flask, and Chroma
