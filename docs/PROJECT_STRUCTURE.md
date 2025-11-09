# Project Lexora - Project Structure

## Directory Organization

```
project-lexora/
├── src/                          # Main source code
│   ├── __init__.py
│   ├── core/                     # Core RAG functionality
│   │   ├── __init__.py
│   │   ├── query_engine.py       # Query processing and RAG retrieval
│   │   └── rag_pipeline.py       # Document loading, splitting, database population
│   ├── models/                   # Model and embedding factories
│   │   ├── __init__.py
│   │   ├── embedding_factory.py  # Embedding function creation
│   │   └── llm_factory.py        # LLM model creation
│   ├── database/                 # Database and vector store
│   │   ├── __init__.py
│   │   ├── vector_store.py       # Abstract vector store interface
│   │   └── chroma_manager.py     # Chroma database implementation
│   └── utils/                    # Utility modules
│       ├── __init__.py
│       ├── config_loader.py      # Configuration management
│       └── logger.py             # Logging utility
│
├── scripts/                      # Executable scripts
│   ├── populate_database.py      # Load PDFs and populate vector DB
│   └── query.py                  # Execute queries against RAG system
│
├── tests/                        # Test suite
│   ├── __init__.py
│   └── test_rag.py              # RAG system tests
│
├── data/                         # PDF data directory
│   ├── cyber_crime_data.pdf
│   └── ipc_sections_data.pdf
│
├── chroma_db/                    # Vector database (auto-generated)
│   └── [Chroma database files]
│
├── config/                       # Configuration files
│   └── [Config files - if needed]
│
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md           # System architecture
│   ├── API_REFERENCE.md          # API documentation
│   └── USAGE_GUIDE.md            # User guide
│
├── .env                          # Environment variables
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── README.md                     # Project README
```

## Module Descriptions

### src/core/
- **query_engine.py**: Handles user queries, retrieves relevant documents, and generates responses using LLM
- **rag_pipeline.py**: Manages document loading, chunking, and database population workflow

### src/models/
- **embedding_factory.py**: Creates and manages embedding functions for vector encoding
- **llm_factory.py**: Creates and configures LLM instances for response generation

### src/database/
- **vector_store.py**: Abstract interface for vector storage implementations
- **chroma_manager.py**: Concrete implementation using Chroma vector database

### src/utils/
- **config_loader.py**: Loads and manages application configuration from environment
- **logger.py**: Centralized logging utility

### scripts/
- **populate_database.py**: CLI script to load PDFs and populate Chroma database
- **query.py**: CLI script to query the RAG system

### tests/
- **test_rag.py**: Comprehensive test suite with 14 test cases

## Usage

### Populate Database
```bash
python scripts/populate_database.py --reset
```

### Execute Query
```bash
python scripts/query.py "Your question here"
```

### Run Tests
```bash
python tests/test_rag.py
# or with pytest
pytest tests/test_rag.py -v
```

## Dependencies
See `requirements.txt` for all dependencies. Key libraries:
- langchain - LLM framework
- langchain-openai - OpenAI integration
- langchain-chroma - Chroma vector store
- python-dotenv - Environment management
