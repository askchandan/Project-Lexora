import argparse
import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from get_embedding_function import get_embedding_function


# load .env
load_dotenv()
CHROMA_PATH = os.getenv('CHROMA_PATH')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_BASE = os.getenv('OPENAI_API_BASE')


PROMPT_TEMPLATE = """Answer the question based only on the following context:

{context}

---

Question: {question}

Answer:"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt = PROMPT_TEMPLATE.format(context=context_text, question=query_text)
    
    model = ChatOpenAI(
        model="mistralai/mistral-7b-instruct",
        temperature=0.7,
        max_tokens=500,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_API_BASE
    )
    
    # Use direct message format
    messages = [
        SystemMessage(content="You are a helpful legal assistant. Answer questions based only on the provided context."),
        HumanMessage(content=prompt)
    ]
    
    response = model.invoke(messages)
    response_text = response.content if hasattr(response, 'content') else str(response)
    response_text = response_text.strip()

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text


if __name__ == "__main__":
    main()
