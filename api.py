from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging

# Import our modules
from scraper import BrainloxScraper
from embeddings import EmbeddingManager
from chatbot import BrainloxChatbot

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
api = Api(app)

# Initialize components
scraper = BrainloxScraper()
embedding_manager = EmbeddingManager()

# Try to load existing vector store, or create a new one
vector_store = embedding_manager.load_vector_store()
if vector_store is None:
    logger.info("No existing vector store found. Creating new embeddings with Mistral AI...")
    documents = scraper.scrape_and_split()
    vector_store = embedding_manager.create_embeddings(documents)
    embedding_manager.save_vector_store()

# Initialize chatbot with Mistral AI
chatbot = BrainloxChatbot(vector_store)

class ChatResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            
            if not data or 'query' not in data:
                return jsonify({"error": "Query parameter is required"}), 400
                
            query = data['query']
            response = chatbot.get_response(query)
            
            return jsonify({
                "response": response,
                "status": "success"
            })
        except Exception as e:
            logger.error(f"Error in ChatResource: {str(e)}")
            return jsonify({
                "error": str(e),
                "status": "error"
            }), 500
            
class ResetConversationResource(Resource):
    def post(self):
        try:
            chatbot.reset_conversation()
            return jsonify({
                "message": "Conversation reset successfully",
                "status": "success"
            })
        except Exception as e:
            logger.error(f"Error in ResetConversationResource: {str(e)}")
            return jsonify({
                "error": str(e),
                "status": "error"
            }), 500

# Add resources to API
api.add_resource(ChatResource, '/api/chat')
api.add_resource(ResetConversationResource, '/api/reset')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)