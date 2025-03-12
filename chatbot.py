import os
from langchain.memory import ConversationBufferMemory  # Update this import based on the new memory class
from langchain_mistralai import ChatMistralAI
from langchain.chains import ConversationalRetrievalChain
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BrainloxChatbot:
    def __init__(self, vector_store, api_key=None, model_name="mistral-large-latest"):
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("Mistral API key is required. Set it in the .env file or pass it directly.")
            
        self.vector_store = vector_store
        self.model_name = model_name
        
        # Initialize the Mistral language model
        self.llm = ChatMistralAI(
            temperature=0.2,
            model=self.model_name,
            api_key=self.api_key
        )
        
        # Create conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Create the conversational chain
        self.conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            memory=self.memory,
            verbose=True
        )
        
        logger.info("Mistral AI Chatbot initialized successfully")
        
    def get_response(self, query):
        """
        Get a response from the chatbot for a given query
        """
        try:
            logger.info(f"Processing query with Mistral AI: {query}")
            response = self.conversation_chain({"question": query})
            logger.info("Response generated successfully")
            return response["answer"]
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"I'm sorry, I encountered an error: {str(e)}"
            
    def reset_conversation(self):
        """
        Reset the conversation memory
        """
        self.memory.clear()
        logger.info("Conversation memory cleared")