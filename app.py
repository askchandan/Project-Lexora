import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader


# load .env
load_dotenv()
DATA_PATH = os.getenv('DATA_PATH')



def load_documents():
    loader = PyPDFLoader(DATA_PATH)
    return loader.load()

