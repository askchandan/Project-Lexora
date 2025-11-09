# Project Lexora - Complete Project Structure Overview

## 📁 Directory Tree

```
project-lexora/
│
├── src/                          # 🎯 Main Application Code
│   ├── __init__.py
│   │
│   ├── core/                     # 🧠 Core RAG Functionality
│   │   ├── __init__.py
│   │   ├── rag_pipeline.py       # Document loading, splitting, DB population
│   │   └── query_engine.py       # Query processing and response generation
│   │
│   ├── models/                   # 🤖 Model & Embedding Management
│   │   ├── __init__.py
│   │   ├── embedding_factory.py  # OpenAI embeddings creation
│   │   └── llm_factory.py        # LLM model configuration
│   │
│   ├── database/                 # 💾 Vector Store Management
│   │   ├── __init__.py
│   │   ├── vector_store.py       # Abstract interface
│   │   └── chroma_manager.py     # Chroma implementation
│   │
│   └── utils/                    # 🛠️ Utilities
│       ├── __init__.py
│       ├── config_loader.py      # Configuration management
│       └── logger.py             # Logging utility
│
├── scripts/                      # 🚀 Executable Scripts
│   ├── populate_database.py      # Load PDFs → Create embeddings → Store
│   └── query.py                  # Execute queries against RAG system
│
├── tests/                        # ✅ Test Suite (14 Tests)
│   ├── __init__.py
│   └── test_rag.py              # Comprehensive test cases
│
├── data/                         # 📄 PDF Documents (Input)
│   ├── cyber_crime_data.pdf
│   └── ipc_sections_data.pdf
│
├── chroma_db/                    # 🗄️ Vector Database (Auto-generated)
│   └── [Chroma persistent storage]
│
├── docs/                         # 📚 Documentation
│   ├── PROJECT_STRUCTURE.md      # This file
│   ├── ARCHITECTURE.md           # System design details
│   ├── USAGE_GUIDE.md            # Step-by-step usage
│   └── TEST_DOCUMENTATION.md     # Test suite details
│
├── config/                       # ⚙️ Configuration Files
│   └── [Placeholder for future config files]
│
├── .env                          # 🔐 Environment Variables (Not in repo)
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── LICENSE                       # MIT License
├── README.md                     # Project overview
└── venv/                         # Virtual environment (excluded)
```

## 🎯 Module Purpose & Responsibilities

### src/core/ - Core Application Logic

**rag_pipeline.py** (RAGPipeline Class)
- Purpose: Manage document processing workflow
- Responsibilities:
  - Load PDFs from directory
  - Split documents into chunks
  - Calculate unique chunk IDs
  - Add chunks to vector database
  - Clear/reset database
- Entry Point: `scripts/populate_database.py`

**query_engine.py** (QueryEngine Class)
- Purpose: Handle user queries and response generation
- Responsibilities:
  - Accept user queries
  - Retrieve relevant documents via similarity search
  - Format prompts for LLM
  - Generate responses using language model
  - Track source documents
- Entry Point: `scripts/query.py`

### src/models/ - AI Model Integration

**embedding_factory.py**
- Purpose: Create embedding functions
- Factory Pattern: Single responsibility for embedding creation
- Returns: OpenAI embeddings instance
- Used By: Both RAGPipeline and QueryEngine

**llm_factory.py**
- Purpose: Create configured LLM instances
- Configuration: Model name, temperature, max tokens, API keys
- Factory Pattern: Centralized LLM instantiation
- Supports: OpenAI, Mistral (via OpenRouter)

### src/database/ - Vector Storage

**vector_store.py** (Abstract Base Class)
- Purpose: Define interface for vector stores
- Methods: add_documents, similarity_search, delete_all
- Design Pattern: Abstract Factory for extensibility

**chroma_manager.py** (ChromaManager Class)
- Purpose: Manage Chroma vector database
- Implements: VectorStore abstract interface
- Features:
  - Add documents with IDs
  - Semantic similarity search
  - Document count tracking
  - Database reset capability

### src/utils/ - Utilities & Configuration

**config_loader.py**
- Purpose: Centralized configuration management
- Sources: Environment variables and .env file
- Returns: Dictionary with all config values
- Settings:
  - API credentials
  - Data paths
  - Model parameters
  - Temperature & token limits

**logger.py**
- Purpose: Centralized logging
- Features: Formatted output with timestamps
- Used By: All modules for consistent logging
- Levels: DEBUG, INFO, WARNING, ERROR

## 📊 Data Flow Diagrams

### Database Population Flow
```
User: python scripts/populate_database.py --reset
         ↓
RAGPipeline.clear_database() [Optional: Remove old data]
         ↓
RAGPipeline.load_documents() → PyPDF reads PDFs
         ↓
RAGPipeline.split_documents() → Chunks with 800 char size
         ↓
RAGPipeline._calculate_chunk_ids() → Create unique IDs
         ↓
RAGPipeline.add_chunks_to_database() → ChromaManager adds to DB
         ↓
ChromaManager.add_documents() → Embeddings created → Stored
         ↓
Console: "Successfully added X documents"
```

### Query Processing Flow
```
User: python scripts/query.py "Your question"
         ↓
QueryEngine initialized with chroma_path
         ↓
QueryEngine.query(query_text, top_k=5)
         ↓
ChromaManager.similarity_search() → Top 5 similar docs
         ↓
Context extracted from documents
         ↓
Prompt formatted with context + question
         ↓
LLM.invoke(messages) → ChatOpenAI generates response
         ↓
Answer + sources returned
         ↓
Console: Display answer and source PDFs
```

## 🔧 Configuration Management

### Environment Variables (.env)
```env
# API Configuration
OPENAI_API_KEY=sk-...
OPENAI_API_BASE=https://openrouter.ai/api/v1

# Data Paths
DATA_PATH=data
CHROMA_PATH=chroma_db

# Model Settings
MODEL_NAME=mistralai/mistral-7b-instruct
TEMPERATURE=0.7
MAX_TOKENS=500
```

### Config Loading Sequence
```
.env File → load_dotenv() → load_config() → Dict → Used by all modules
```

## 🧪 Test Suite (14 Tests)

Location: `tests/test_rag.py`

Test Categories:
1. **Specific Offenses** (8 tests)
   - Hacking punishment
   - Computer resource cheating
   - Private image publishing
   - Cyberterrorism
   - Source code tampering
   - Stolen device
   - Password misuse
   - Protected system access

2. **Section Details** (2 tests)
   - Section 65 details
   - Section 66 details

3. **Response Quality** (4 tests)
   - Response validity
   - Multiple crimes listing
   - Fine amounts extraction
   - Imprisonment duration

## 🔌 Integration Points

### External Services
1. **OpenAI/OpenRouter**: LLM and embeddings
2. **PDF Source**: Local files in `data/` directory

### Internal Integration
```
QueryEngine ← LLMFactory
QueryEngine ← ChromaManager
ChromaManager ← EmbeddingFactory
RAGPipeline ← ChromaManager
RAGPipeline ← TextSplitter
All Modules ← ConfigLoader
All Modules ← Logger
```

## 📈 Scalability Path

### Current Capacity
- Documents: Thousands
- Queries: Sequential
- Response Time: 2-5 seconds

### Future Scaling
1. **Async Processing**: Queue for batch document processing
2. **Caching**: Cache frequent queries
3. **Multi-Model**: Support multiple embedding models
4. **Distributed**: Separate embedding, search, and generation services
5. **UI**: Web interface for easier access

## 🚀 Getting Started - Quick Reference

### Setup
```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure
# Edit .env with API keys

# 3. Populate
python scripts/populate_database.py --reset

# 4. Query
python scripts/query.py "Your question"

# 5. Test
python tests/test_rag.py
```

### File Locations
- Source Code: `src/`
- Scripts: `scripts/`
- Tests: `tests/`
- Data: `data/`
- Database: `chroma_db/`
- Docs: `docs/`

## 📝 Module Dependencies

```
main
├── populate_database.py
│   └── src.core.rag_pipeline
│       ├── src.database.chroma_manager
│       ├── src.models.embedding_factory
│       └── src.utils
│
├── query.py
│   └── src.core.query_engine
│       ├── src.database.chroma_manager
│       ├── src.models.llm_factory
│       └── src.utils
│
└── test_rag.py
    └── src.core.query_engine
        └── [same as query.py]
```

## ✨ Key Features by Module

| Module | Feature |
|--------|---------|
| RAGPipeline | Document management and indexing |
| QueryEngine | Semantic search and response generation |
| EmbeddingFactory | Consistent embedding generation |
| LLMFactory | Configurable LLM creation |
| ChromaManager | Fast vector similarity search |
| ConfigLoader | Environment-based configuration |
| Logger | Consistent logging across modules |

---

**Project Lexora** - Professional RAG System Architecture
