"""
Query engine for RAG-based question answering
"""

from typing import List, Tuple, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from src.database.chroma_manager import ChromaManager
from src.models import get_llm_model
from src.utils import get_logger

logger = get_logger(__name__)


SYSTEM_MESSAGE = "You are a helpful legal assistant. Answer questions based only on the provided context."

PROMPT_TEMPLATE = """Answer the question based only on the following context:

{context}

---

Question: {question}

Answer:"""


class QueryEngine:
    """Handles query processing and RAG-based retrieval"""
    
    def __init__(self, chroma_path: str, model_name: str = "mistralai/mistral-7b-instruct"):
        """
        Initialize query engine.
        
        Args:
            chroma_path: Path to Chroma database
            model_name: LLM model to use
        """
        self.vector_store = ChromaManager(chroma_path)
        self.llm = get_llm_model(model_name=model_name)
        logger.info(f"Initialized Query Engine with model {model_name}")
    
    def query(self, query_text: str, top_k: int = 5) -> Tuple[str, List[str]]:
        """
        Execute a query against the RAG system.
        
        Args:
            query_text: User query
            top_k: Number of relevant documents to retrieve
        
        Returns:
            Tuple of (answer, source_ids)
        """
        logger.info(f"Processing query: {query_text[:50]}...")
        
        # Retrieve relevant documents
        results = self.vector_store.similarity_search(query_text, k=top_k)
        
        if not results:
            logger.warning("No relevant documents found")
            return "No relevant information found in the database.", []
        
        # Extract context and sources
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        sources = [doc.metadata.get("id", "Unknown") for doc, _score in results]
        
        # Format prompt
        prompt = PROMPT_TEMPLATE.format(context=context_text, question=query_text)
        
        # Generate response
        messages = [
            SystemMessage(content=SYSTEM_MESSAGE),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        answer = response.content.strip() if hasattr(response, 'content') else str(response)
        
        logger.info(f"Generated response with {len(sources)} sources")
        
        return answer, sources
