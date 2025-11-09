# Project Lexora - Getting Started Guide

## Installation

### 1. Prerequisites
- Python 3.10+
- pip package manager
- Virtual environment (recommended)

### 2. Setup Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Configuration

### 1. Environment Setup
Create a `.env` file in the project root:

```env
# API Configuration
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE=https://openrouter.ai/api/v1

# Data Paths
DATA_PATH=data
CHROMA_PATH=chroma_db

# Model Configuration
MODEL_NAME=mistralai/mistral-7b-instruct
TEMPERATURE=0.7
MAX_TOKENS=500
```

### 2. Required API Keys
- **OpenAI API Key**: Get from https://platform.openai.com
- **OpenRouter (Optional)**: For alternative models

## Quick Start

### Step 1: Populate Database
Load PDF documents into the vector database:

```bash
# First time setup
python scripts/populate_database.py --reset

# Subsequent runs
python scripts/populate_database.py
```

### Step 2: Query the System
Ask questions about the documents:

```bash
python scripts/query.py "What is the punishment for hacking?"
```

### Step 3: Run Tests
Verify the system is working correctly:

```bash
python tests/test_rag.py
```

## Usage Examples

### Example 1: Legal Query
```bash
python scripts/query.py "What is Section 66 of the IT Act?"
```

Output:
```
======================================================================
RESPONSE
======================================================================
Section 66 deals with hacking. It states that if a person destroys, 
deletes, or alters information in a computer to cause wrongful damage...

----------------------------------------------------------------------
SOURCES
----------------------------------------------------------------------
  - data\cyber_crime_data.pdf:0:0
  - data\cyber_crime_data.pdf:1:0
======================================================================
```

### Example 2: Specific Punishment Query
```bash
python scripts/query.py "What is the fine for cheating using computer resource?"
```

### Example 3: Retrieve Multiple Offenses
```bash
python scripts/query.py "List all cyber crimes and their punishments"
```

## Common Issues & Solutions

### Issue 1: ModuleNotFoundError
```
ModuleNotFoundError: No module named 'langchain_chroma'
```
**Solution**: Reinstall requirements
```bash
pip install -r requirements.txt
```

### Issue 2: Empty Responses
```
Response: 
Sources: [...]
```
**Solution**: 
- Ensure database is populated: `python scripts/populate_database.py`
- Check API key is valid in `.env`
- Verify model name is correct

### Issue 3: API Key Error
```
Could not load credentials to authenticate with AWS
```
**Solution**: 
- Use OpenAI API key, not AWS
- Update `.env` with correct keys

## Project Structure Quick Reference

```
src/           - Main application code
scripts/       - Executable scripts (populate, query)
tests/         - Test suite
data/          - PDF documents (input)
chroma_db/     - Vector database (auto-generated)
docs/          - Documentation
```

## Next Steps

1. **Add Your Documents**: Place PDF files in `data/` directory
2. **Customize Model**: Adjust `MODEL_NAME` in `.env`
3. **Tune Performance**: Modify `TEMPERATURE` and `MAX_TOKENS`
4. **Extend Functionality**: Add new query types in `src/core/query_engine.py`

## Getting Help

- Check documentation in `/docs`
- Review test cases in `/tests/test_rag.py`
- Enable debug logging by setting `LOG_LEVEL=DEBUG`
