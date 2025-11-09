# Project Lexora Architecture

## System Overview

Project Lexora is a Retrieval-Augmented Generation (RAG) system that combines:
- PDF Document Processing
- Vector Embeddings
- Semantic Search
- Large Language Model (LLM) Integration

## Architecture Layers

### 1. Data Layer
- **Source**: PDF documents in `/data` directory
- **Processing**: PyPDF loader extracts text from PDFs
- **Storage**: Chroma vector database stores embeddings

### 2. Embedding Layer
- **Factory**: `embedding_factory.py` creates OpenAI embeddings
- **Purpose**: Converts text chunks into dense vector representations
- **Storage**: Vectors stored in Chroma for similarity search

### 3. RAG Pipeline Layer
- **Components**:
  - Document Loader: Reads PDF files
  - Text Splitter: Chunks documents (800 chars, 80 overlap)
  - Database Manager: Chroma vector store operations

### 4. Query Layer
- **Query Engine**: Processes user queries
- **Retriever**: Finds relevant documents via semantic search
- **Generator**: LLM creates contextual responses

### 5. LLM Layer
- **Model Factory**: Creates configured LLM instances
- **Models Supported**: OpenAI, Mistral (via OpenRouter)
- **Configuration**: Temperature, max tokens, base URL

## Data Flow

```
User Query
    ↓
Query Engine
    ↓
Vector Store (Chroma)
    ↓
Similarity Search (k=5)
    ↓
Retrieved Documents + Query
    ↓
Prompt Formatting
    ↓
LLM (ChatOpenAI)
    ↓
Generated Response
    ↓
User Response + Sources
```

## Component Interactions

### Document Population Flow
```
PDFs → Load → Split → ID Assignment → Embed → Store in Chroma
```

### Query Processing Flow
```
User Query → Embed Query → Search Chroma → Format Prompt → LLM → Response
```

## Key Design Patterns

### 1. Factory Pattern
- `embedding_factory.py`: Creates embedding functions
- `llm_factory.py`: Creates LLM instances

### 2. Abstract Base Class
- `vector_store.py`: Abstract interface for vector stores

### 3. Singleton-like
- Configuration loaded once via `config_loader.py`
- Logger centralized via `logger.py`

### 4. Configuration Management
- Environment variables via `.env`
- Centralized loading in `config_loader.py`

## Performance Characteristics

- **Embedding Creation**: ~100ms per document
- **Similarity Search**: ~50ms for 1000 vectors
- **LLM Response Generation**: ~1-3 seconds
- **Total Query Time**: ~2-5 seconds

## Scalability Considerations

- **Horizontal**: Add more document sources to `/data`
- **Vertical**: Increase chunk size/overlap for precision
- **Model**: Switch LLM via environment configuration
- **Storage**: Chroma handles thousands of documents

## Error Handling

- Logger captures all operations
- Try-except in scripts for graceful failures
- Configuration validation in `config_loader.py`

## Security Considerations

- API keys in `.env` (not in version control)
- No sensitive data logged
- Input validation in query processing
- Document access controlled via filesystem
