# 🧪 Testing Your Chatbot - Complete Guide

## 📊 Testing Levels

```
Unit Tests (14 tests)
    ↓
Integration Tests (Query system)
    ↓
Manual Testing (CLI)
    ↓
Production Testing (Real queries)
```

---

## 1️⃣ **Automated Test Suite** (Recommended First Step)

### ✅ Run All Tests
```powershell
cd "C:\Users\Chandan Malakar\Desktop\PDF AI Chat"
python tests/test_rag.py
```

### 📋 What Gets Tested (14 Tests):

**Specific IT Act Sections:**
1. ✅ `test_hacking_punishment` - Section 66: Hacking punishment
2. ✅ `test_cheating_using_computer_resource` - Section 66D: Computer cheating
3. ✅ `test_publishing_private_images` - Section 66E: Privacy violation
4. ✅ `test_cyberterrorism_offense` - Section 66F: Cyberterrorism
5. ✅ `test_tampering_with_source_code` - Section 65: Source code tampering
6. ✅ `test_receiving_stolen_computer` - Section 66B: Stolen device
7. ✅ `test_unauthorized_password_usage` - Section 66C: Password misuse
8. ✅ `test_protected_system_access` - Section 70: Protected system

**Section Details:**
9. ✅ `test_section_65_details` - Complete Section 65 info
10. ✅ `test_section_66_details` - Complete Section 66 info

**Response Quality:**
11. ✅ `test_response_contains_sources` - Verify source attribution
12. ✅ `test_multiple_cyber_crimes` - Handle multiple topics
13. ✅ `test_fine_amounts` - Extract punishment amounts
14. ✅ `test_imprisonment_duration` - Extract jail duration

### 📊 Expected Output:
```
[PASS] Hacking punishment
[PASS] Cheating using computer resource
[PASS] Publishing private images
[PASS] Cyberterrorism offense
[PASS] Tampering with source code
[PASS] Receiving stolen computer
[PASS] Unauthorized password usage
[PASS] Protected system access
[PASS] Section 65 details
[PASS] Section 66 details
[PASS] Response contains sources
[PASS] Multiple cyber crimes
[PASS] Fine amounts
[PASS] Imprisonment duration

✅ ALL TESTS PASSED (14/14)
```

---

## 2️⃣ **Interactive CLI Testing** (Manual Testing)

### 🚀 Start a Query Session
```powershell
python scripts/query.py "What is the punishment for hacking?"
```

### 📝 Example Test Queries:

**Basic Queries:**
```bash
# Test 1: Direct question
python scripts/query.py "What is Section 66?"

# Test 2: Punishment query
python scripts/query.py "What is the imprisonment for cyberterrorism?"

# Test 3: Fine query
python scripts/query.py "What are the fines for computer cheating?"

# Test 4: Definition query
python scripts/query.py "Define unauthorized access to computer system"

# Test 5: Complex query
python scripts/query.py "What are the penalties for hacking and stealing data?"
```

### ✅ What to Check in Responses:

- ✓ **Relevance**: Does it answer your question?
- ✓ **Accuracy**: Is the legal information correct?
- ✓ **Completeness**: Does it mention imprisonment AND fines?
- ✓ **Sources**: Does it show which PDF it came from?
- ✓ **Format**: Is it well-organized and readable?

### Example Response Format:
```
Answer:
According to Section 66 of the IT Act, unauthorized access to computer 
systems is punishable with imprisonment up to 3 years and/or fine up to 
500,000 rupees...

Sources:
- cyber_crime_data.pdf (Page 2)
```

---

## 3️⃣ **Database Verification**

### 🗄️ Check Database Population
```powershell
# Reset and repopulate database
python scripts/populate_database.py --reset
```

### 📊 Expected Output:
```
Loaded 2 documents from data/
Split into X chunks
Successfully added X documents to Chroma database
```

### ✅ Verification Checks:
```python
# Open Python interpreter
python

# Check document count
from src.database.chroma_manager import ChromaManager
cm = ChromaManager(chroma_path="chroma_db")
count = cm.get_document_count()
print(f"Total documents in database: {count}")
# Expected: 100+ documents

# Test similarity search
results = cm.similarity_search("hacking punishment", k=5)
print(f"Found {len(results)} similar documents")
# Expected: 5 documents with relevance scores
```

---

## 4️⃣ **Component Testing**

### 🔌 Test Individual Components

#### A. Embedding Factory
```python
from src.models.embedding_factory import get_embedding_function
embeddings = get_embedding_function()
print(f"Embedding model: {embeddings.model}")
# Expected: text-embedding-3-small
```

#### B. LLM Factory
```python
from src.models.llm_factory import get_llm_model
llm = get_llm_model()
response = llm.invoke("What is AI?")
print(response.content)
# Expected: LLM response about AI
```

#### C. Config Loader
```python
from src.utils import load_config
config = load_config()
print(config)
# Expected: All keys present and non-empty
```

#### D. Vector Store
```python
from src.database.chroma_manager import ChromaManager
cm = ChromaManager(chroma_path="chroma_db")
results = cm.similarity_search("hacking", k=3)
print(f"Found {len(results)} results")
# Expected: 3 results with scores
```

---

## 5️⃣ **Performance Testing**

### ⚡ Query Response Time
```python
import time
from src.core.query_engine import QueryEngine
from src.utils import load_config

config = load_config()
engine = QueryEngine(chroma_path=config['chroma_path'])

# Test response time
start = time.time()
answer, sources = engine.query("What is hacking?")
end = time.time()

print(f"Response time: {end - start:.2f} seconds")
# Expected: 1-5 seconds
```

### 🔄 Batch Testing (Multiple Queries)
```python
queries = [
    "What is hacking?",
    "Define unauthorized access",
    "What are cyber crimes?",
    "Section 65 punishment",
    "What is phishing?"
]

for query in queries:
    answer, sources = engine.query(query)
    print(f"✓ {query}")
```

---

## 6️⃣ **Stress Testing**

### 💥 Test with Edge Cases
```python
# Empty query
engine.query("")

# Very long query
engine.query("What is " * 100)

# Special characters
engine.query("What is @#$%^&*()?")

# Multiple languages (if applicable)
engine.query("हैकिंग क्या है?")  # Hindi

# Offensive content
engine.query("Tell me how to hack systems")
```

### Expected Behavior:
- Should handle gracefully
- Return meaningful error messages
- Not crash or hang

---

## 7️⃣ **Quality Assurance Checklist**

### ✅ Pre-Deployment Testing

- [ ] All 14 tests passing
- [ ] Database populated with 100+ documents
- [ ] Query response time < 5 seconds
- [ ] No errors in logs
- [ ] Sources properly attributed
- [ ] Embeddings generating correctly
- [ ] LLM responses relevant to queries
- [ ] Config loaded from .env
- [ ] No sensitive data in console output

### ✅ Response Quality

- [ ] Answers are legally accurate
- [ ] Responses mention Section numbers
- [ ] Penalties (fines/imprisonment) included
- [ ] Sources cited correctly
- [ ] No hallucinated information
- [ ] Formatting is readable

---

## 8️⃣ **Debugging Failed Tests**

### 🔍 If Tests Fail:

#### Step 1: Check Prerequisites
```powershell
# Verify Python
python --version  # Should be 3.8+

# Check dependencies
pip list | findstr "langchain openai chromadb"

# Check .env file
Get-Content .env  # Verify API key exists
```

#### Step 2: Check Database
```powershell
# Repopulate database
python scripts/populate_database.py --reset

# Verify documents loaded
python -c "from src.database.chroma_manager import ChromaManager; cm = ChromaManager(); print(f'Documents: {cm.get_document_count()}')"
```

#### Step 3: Test Components Individually
```python
# Test embeddings
from src.models.embedding_factory import get_embedding_function
emb = get_embedding_function()
test_embedding = emb.embed_query("test")
print(f"Embedding size: {len(test_embedding)}")  # Should be 1536
```

#### Step 4: Check Logs
```powershell
# View recent logs
Get-ChildItem logs/ -Recurse | Sort-Object LastWriteTime -Descending | Select-Object -First 5
```

---

## 9️⃣ **Test Results Interpretation**

### ✅ All Tests Pass
```
Scenario: Perfect ✓
Meaning: System working as expected
Next Step: Deploy to production
```

### ⚠️ Some Tests Fail
```
Scenario: 10/14 tests pass
Meaning: Check specific test failures
Next Step: Debug failing components
```

### ❌ All Tests Fail
```
Scenario: 0/14 tests pass
Meaning: System configuration issue
Likely Causes:
- Database not populated
- API keys incorrect
- Dependencies missing
- .env file misconfigured
```

---

## 🔟 **Recommended Testing Workflow**

### 1️⃣ Initial Setup
```powershell
# Verify installation
python tests/test_rag.py
```

### 2️⃣ After Code Changes
```powershell
# Run tests before committing
python tests/test_rag.py
```

### 3️⃣ Daily Development
```powershell
# Quick manual test
python scripts/query.py "Your test question"
```

### 4️⃣ Before Deployment
```powershell
# Full verification
python scripts/populate_database.py --reset
python tests/test_rag.py
python scripts/query.py "Test query"
```

---

## 📈 Continuous Improvement

### Add More Tests
Create `tests/test_advanced.py`:
```python
def test_performance():
    """Test response time < 3 seconds"""
    import time
    start = time.time()
    engine.query("What is hacking?")
    duration = time.time() - start
    assert duration < 3, f"Response took {duration}s"

def test_context_window():
    """Test with very long queries"""
    long_query = "What is " * 50 + "hacking?"
    response, _ = engine.query(long_query)
    assert len(response) > 0
```

### Monitor Metrics
- Response times
- Accuracy rates
- Source relevance scores
- User satisfaction

---

## 🎯 Summary

| Testing Type | Command | Frequency | Purpose |
|-------------|---------|-----------|---------|
| Automated | `python tests/test_rag.py` | Every commit | Verify functionality |
| Manual | `python scripts/query.py "?"` | Daily | Quality check |
| Integration | Run all scripts | Weekly | Full system test |
| Performance | Measure response time | Weekly | Optimization |
| Regression | Run old test queries | Monthly | Prevent bugs |

---

**Happy Testing! 🚀**
