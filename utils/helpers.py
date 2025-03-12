import logging
import os
import time
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def retry_with_backoff(max_retries=3, initial_backoff=1, backoff_factor=2):
    """
    Retry decorator with exponential backoff for API calls
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            current_backoff = initial_backoff
            
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        logger.error(f"Max retries reached. Last error: {str(e)}")
                        raise
                    
                    logger.warning(f"Retry {retries}/{max_retries} after error: {str(e)}. Backing off for {current_backoff}s")
                    time.sleep(current_backoff)
                    current_backoff *= backoff_factor
                    
        return wrapper
    return decorator

def ensure_dir(directory):
    """
    Ensure directory exists, create if it doesn't
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created directory: {directory}")