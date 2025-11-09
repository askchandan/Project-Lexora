"""
Flask Web Application for Project Lexora
GUI for RAG + LLM Chatbot with PDF Upload
"""

import os
import shutil
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
from src.core.rag_pipeline import RAGPipeline
from src.core.query_engine import QueryEngine
from src.utils import load_config, get_logger

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'project_lexora_secret_key_2024'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

logger = get_logger(__name__)
config = load_config()

# Global pipeline and engine instances
pipeline = None
query_engine = None
chroma_manager = None


def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def initialize_pipeline():
    """Initialize RAG pipeline and query engine"""
    global pipeline, query_engine, chroma_manager
    try:
        logger.info("Initializing RAG Pipeline...")
        pipeline = RAGPipeline(
            data_path=config['data_path'],
            chroma_path=config['chroma_path']
        )
        logger.info("RAG Pipeline initialized successfully")
        
        logger.info("Initializing Chroma Manager...")
        from src.database.chroma_manager import ChromaManager
        chroma_manager = ChromaManager(persist_directory=config['chroma_path'])
        logger.info("Chroma Manager initialized successfully")
        
        logger.info("Initializing Query Engine...")
        query_engine = QueryEngine(
            chroma_path=config['chroma_path'],
            model_name=config.get('model_name', 'mistralai/mistral-7b-instruct')
        )
        logger.info("Query Engine initialized successfully")
        logger.info(f"Initial document count: {chroma_manager.get_document_count()}")
        return True
    except Exception as e:
        logger.error(f"Error initializing pipeline: {str(e)}", exc_info=True)
        return False


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_pdf():
    """Handle PDF upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'message': 'Only PDF files allowed'}), 400
        
        # Save file to uploads folder
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        logger.info(f"PDF file saved: {filename}")
        
        # Process the uploaded PDF
        from langchain_community.document_loaders import PyPDFLoader
        logger.info(f"Loading PDF: {filepath}")
        loader = PyPDFLoader(filepath)
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} pages from PDF")
        
        # Split and add to database
        logger.info("Splitting documents...")
        chunks = pipeline.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks")
        
        logger.info("Adding chunks to database...")
        added_count = pipeline.add_chunks_to_database(chunks)
        logger.info(f"Added {added_count} document chunks to database")
        
        # Reinitialize both query engine and chroma manager to refresh state
        global query_engine, chroma_manager
        logger.info("Reinitializing query engine and chroma manager...")
        
        # Recreate chroma manager to get fresh connection to updated database
        from src.database.chroma_manager import ChromaManager
        chroma_manager = ChromaManager(persist_directory=config['chroma_path'])
        new_count = chroma_manager.get_document_count()
        logger.info(f"✓ Chroma manager refreshed. New document count: {new_count}")
        
        if new_count != added_count:
            logger.warning(f"⚠ Mismatch! Added {added_count} chunks, but total is {new_count}")
        
        query_engine = QueryEngine(
            chroma_path=config['chroma_path'],
            model_name=config.get('model_name', 'mistralai/mistral-7b-instruct')
        )
        logger.info("✓ Query engine reinitialized")
        
        logger.info(f"✓ Upload complete! Total documents in DB: {new_count}")
        
        return jsonify({
            'success': True,
            'message': f'PDF uploaded successfully. Added {added_count} document chunks.',
            'filename': filename,
            'chunks': added_count,
            'total_documents': new_count
        }), 200
        
    except Exception as e:
        logger.error(f"Error uploading PDF: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/query', methods=['POST'])
def query():
    """Handle query requests"""
    try:
        data = request.get_json()
        user_query = data.get('query', '').strip()
        
        if not user_query:
            return jsonify({'success': False, 'message': 'Please enter a question'}), 400
        
        if query_engine is None:
            return jsonify({'success': False, 'message': 'Query engine not initialized'}), 500
        
        logger.info(f"Query received: {user_query[:50]}...")
        
        # Check if database has documents
        global chroma_manager
        if chroma_manager is None:
            return jsonify({'success': False, 'message': 'Database not initialized'}), 500
            
        doc_count = chroma_manager.get_document_count()
        logger.info(f"Current document count: {doc_count}")
        
        if doc_count == 0:
            return jsonify({
                'success': True,
                'answer': 'No documents uploaded yet. Please upload a PDF first.',
                'sources': [],
                'query': user_query
            }), 200
        
        logger.info(f"Executing query: {user_query[:50]}...")
        
        # Execute query with timeout
        answer, sources = query_engine.query(user_query, top_k=5)
        
        logger.info(f"Query executed successfully. Sources: {len(sources)}")
        
        return jsonify({
            'success': True,
            'answer': answer,
            'sources': sources,
            'query': user_query
        }), 200
        
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/status', methods=['GET'])
def status():
    """Get application status"""
    try:
        global chroma_manager
        
        doc_count = 0
        error_msg = None
        
        try:
            if chroma_manager is not None:
                doc_count = chroma_manager.get_document_count()
            else:
                logger.warning("Status request but chroma_manager is None!")
                error_msg = "Database not initialized"
        except Exception as e:
            logger.error(f"Error getting document count: {str(e)}", exc_info=True)
            error_msg = f"Database error: {str(e)}"
            doc_count = 0
        
        model_name = config.get('model_name', 'N/A')
        
        response = {
            'success': error_msg is None,
            'initialized': query_engine is not None and error_msg is None,
            'documents': doc_count,
            'model': model_name
        }
        
        if error_msg:
            response['error'] = error_msg
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error in status endpoint: {str(e)}", exc_info=True)
        return jsonify({
            'success': False, 
            'message': str(e),
            'documents': 0,
            'model': 'Error',
            'error': str(e)
        }), 200  # Return 200 even on error so frontend can handle it


@app.route('/clear', methods=['POST'])
def clear_database():
    """Clear the vector database"""
    try:
        if pipeline is None:
            return jsonify({'success': False, 'message': 'Pipeline not initialized'}), 500
        
        logger.info("Clearing database...")
        pipeline.clear_database()
        
        # Reinitialize both query engine and chroma manager
        global query_engine, chroma_manager
        
        from src.database.chroma_manager import ChromaManager
        chroma_manager = ChromaManager(persist_directory=config['chroma_path'])
        logger.info("Chroma manager reinitialized after clear")
        
        query_engine = QueryEngine(
            chroma_path=config['chroma_path'],
            model_name=config.get('model_name', 'mistralai/mistral-7b-instruct')
        )
        logger.info("Query engine reinitialized after clear")
        
        # Clear uploads folder
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        
        logger.info("Database and uploads cleared successfully")
        
        return jsonify({
            'success': True,
            'message': 'Database cleared successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Error clearing database: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    # Initialize pipeline on startup
    if initialize_pipeline():
        logger.info("Pipeline initialized successfully")
        print("✓ Pipeline initialized")
    else:
        print("✗ Failed to initialize pipeline")
    
    # Run Flask app
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
        use_reloader=False
    )
