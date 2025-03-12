# filepath: d:\AI\langchain-chatbot\embeddings.py
import os
from dotenv import load_dotenv
import faiss
import logging
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema.document import Document

# Load environment variables from .env file
load_dotenv()

# Print to verify environment variables
print("HF_TOKEN:", os.getenv("HF_TOKEN"))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EmbeddingManager:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("Mistral API key is required. Set it in the .env file or pass it directly.")
        
        # Initialize Mistral embeddings
        self.embeddings = MistralAIEmbeddings(
            api_key=self.api_key,
            model="mistral-embed"  # Using Mistral's embedding model
        )
        self.vector_store = None
        self.vector_store_path = "vector_store"

    def create_embeddings(self, documents):
        """
        Create embeddings from documents and store them in FAISS.
        """
        try:
            logger.info(f"Creating embeddings for {len(documents)} documents using Mistral AI")
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
            logger.info("Embeddings created successfully")
            return self.vector_store
        except Exception as e:
            logger.error(f"Error creating embeddings: {str(e)}")
            raise e
            
    def save_vector_store(self, path=None):
        """
        Save the FAISS vector store to disk.
        """
        if self.vector_store is None:
            raise ValueError("Vector store is not initialized. Create embeddings first.")
            
        save_path = path or self.vector_store_path
        try:
            self.vector_store.save_local(save_path)
            logger.info(f"Vector store saved to {save_path}")
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")
            raise e
            
    def load_vector_store(self, path=None):
        """
        Load the FAISS vector store from disk.
        """
        load_path = path or self.vector_store_path
        try:
            if os.path.exists(load_path):
                self.vector_store = FAISS.load_local(
                    load_path, 
                    self.embeddings, 
                    allow_dangerous_deserialization=True  # FIX: Allows loading the FAISS store
                )
                logger.info(f"Vector store loaded from {load_path}")
                return self.vector_store
            else:
                logger.warning(f"Vector store file not found at {load_path}")
                return None
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            raise e