import os
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BrainloxScraper:
    def __init__(self, base_url="https://brainlox.com/courses/category/technical"):
        self.base_url = base_url
        self.loader = WebBaseLoader(web_paths=[self.base_url])
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
    def scrape_and_split(self):
        """
        Scrape the website and split the content into manageable chunks
        """
        try:
            logger.info(f"Starting to scrape {self.base_url}")
            documents = self.loader.load()
            logger.info(f"Successfully scraped {len(documents)} documents")
            
            # Split documents into chunks
            splits = self.text_splitter.split_documents(documents)
            logger.info(f"Split documents into {len(splits)} chunks")
            
            return splits
        except Exception as e:
            logger.error(f"Error scraping website: {str(e)}")
            raise e