# Project Lexora

**An Intelligent PDF Analysis and Chat System powered by LLM + RAG**

A production-ready Retrieval-Augmented Generation (RAG) system that enables natural language querying of PDF documents with AI-powered responses.

## Features

✅ **Document Processing**: Automatically loads and indexes PDF documents  
✅ **Semantic Search**: Finds relevant documents using vector similarity  
✅ **AI-Powered Responses**: Generates contextual answers using LLM  
✅ **Multi-Source Tracking**: Shows source documents for each answer  
✅ **Comprehensive Testing**: 14+ test cases ensuring reliability  
✅ **Modular Architecture**: Clean, maintainable, extensible codebase  
✅ **Configuration Management**: Easy environment-based configuration  

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Create `.env` file with:
```env
OPENAI_API_KEY=your_key
OPENAI_API_BASE=https://openrouter.ai/api/v1
DATA_PATH=data
CHROMA_PATH=chroma_db
```

### 3. Populate Database
```bash
python scripts/populate_database.py --reset
```

### 4. Ask Questions
```bash
python scripts/query.py "What is the punishment for hacking?"
```

## Architecture

### Core Components

1. **Document Pipeline** (`src/core/rag_pipeline.py`)
   - Load PDFs from data directory
   - Split into chunks for processing
   - Generate embeddings
   - Store in vector database

2. **Query Engine** (`src/core/query_engine.py`)
   - Process user queries
   - Retrieve relevant documents
   - Generate AI responses

3. **Embedding System** (`src/models/embedding_factory.py`)
   - OpenAI embeddings for semantic understanding
   - Vector similarity search

4. **Vector Database** (`src/database/chroma_manager.py`)
   - Chroma for fast similarity search
   - Persistent storage of embeddings

5. **LLM Integration** (`src/models/llm_factory.py`)
   - Configurable language models
   - OpenAI and Mistral support

## Project Structure

```
project-lexora/
├── src/                    # Source code
│   ├── core/              # RAG pipeline & query engine
│   ├── models/            # Embedding & LLM factories
│   ├── database/          # Vector store management
│   └── utils/             # Configuration & logging
├── scripts/               # Executable scripts
│   ├── populate_database.py
│   └── query.py
├── tests/                 # Test suite (14 test cases)
├── data/                  # PDF documents (input)
├── docs/                  # Documentation
└── config/               # Configuration files
```

## Usage Examples

### Query for Legal Information
```bash
python scripts/query.py "What is Section 66 of IT Act?"
```

### List Multiple Topics
```bash
python scripts/query.py "List all cyber crimes and their penalties"
```

### Refresh Database
```bash
python scripts/populate_database.py --reset
```

### Run Tests
```bash
python tests/test_rag.py
```

## Test Coverage

14 comprehensive test cases covering:
- ✅ Hacking punishment retrieval
- ✅ Computer resource cheating
- ✅ Private image publishing
- ✅ Cyberterrorism definitions
- ✅ Source code tampering
- ✅ Stolen device handling
- ✅ Password misuse
- ✅ Protected system access
- ✅ Section-specific details
- ✅ Multi-topic queries
- ✅ Fine amount extraction
- ✅ Imprisonment duration
- ✅ Response validation
- ✅ Source tracking

## Configuration

### Environment Variables

```env
# API Configuration
OPENAI_API_KEY=sk-...              # OpenAI or OpenRouter API key
OPENAI_API_BASE=https://...        # API base URL

# Data Configuration
DATA_PATH=data                      # PDF directory path
CHROMA_PATH=chroma_db              # Vector DB path

# Model Configuration
MODEL_NAME=mistralai/mistral-7b-instruct
TEMPERATURE=0.7                    # Creativity (0-1)
MAX_TOKENS=500                     # Response length
```

## Performance

- **Database Population**: ~100ms per document
- **Query Processing**: 2-5 seconds (including API calls)
- **Similarity Search**: <50ms for 1000+ vectors
- **Supported Docs**: Thousands of documents

## API Reference

### Query Engine
```python
from src.core.query_engine import QueryEngine

engine = QueryEngine(chroma_path="chroma_db")
answer, sources = engine.query("Your question", top_k=5)
```

### RAG Pipeline
```python
from src.core.rag_pipeline import RAGPipeline

pipeline = RAGPipeline(data_path="data", chroma_path="chroma_db")
documents = pipeline.load_documents()
chunks = pipeline.split_documents(documents)
pipeline.add_chunks_to_database(chunks)
```

## Documentation

- [Project Structure](docs/PROJECT_STRUCTURE.md) - Directory organization
- [Architecture](docs/ARCHITECTURE.md) - System design
- [Usage Guide](docs/USAGE_GUIDE.md) - Detailed instructions

## Dependencies

Core dependencies:
- `langchain` - LLM framework
- `langchain-openai` - OpenAI integration
- `langchain-chroma` - Vector database
- `pypdf` - PDF processing
- `python-dotenv` - Configuration management

See `requirements.txt` for complete list.

## Error Handling

The system includes:
- Comprehensive logging
- Graceful error handling
- Configuration validation
- Empty response fallbacks

## Security

- API keys stored in `.env` (gitignored)
- No sensitive data logging
- Input validation
- Secure document storage

## Future Enhancements

- [ ] Web UI interface
- [ ] Support for more document types
- [ ] Advanced filtering options
- [ ] Custom fine-tuning
- [ ] Multi-language support
- [ ] Real-time document updates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python tests/test_rag.py`
5. Submit a pull request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues or questions:
1. Check the [Usage Guide](docs/USAGE_GUIDE.md)
2. Review test cases in `tests/test_rag.py`
3. Check system logs for errors

---

**Project Lexora** - Intelligent PDF Analysis & Chat System  
Built with LangChain, OpenAI, and Chroma
