# Brainlox Course Assistant

A smart chatbot that helps users discover and learn about technical courses available on Brainlox.com.

## Features

- 🔍 **Web Scraping**: Automatically extracts course information from Brainlox
- 🧠 **Mistral AI Integration**: Leverages Mistral AI models for intelligent responses
- 🔄 **Vector Database**: Stores course information in a FAISS vector database for semantic search
- 🔌 **RESTful API**: Flask-based API for easy integration with any front-end
- 💻 **Streamlit UI**: Beautiful and responsive user interface

## Architecture

This project combines several powerful technologies:

1. **LangChain**: Framework for building applications with Large Language Models
2. **Mistral AI**: Advanced language models for natural language understanding and generation
3. **FAISS**: Vector database for efficient similarity search
4. **Flask**: API backend for handling chat requests
5. **Streamlit**: Interactive frontend for user engagement

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/brainlox-course-assistant.git
   cd brainlox-course-assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables (create a `.env` file):
   ```
   MISTRAL_API_KEY=your-mistral-ai-api-key
   API_URL=http://localhost:5000/api
   ```

## Usage

1. Start the Flask API server:
   ```bash
   python api.py
   ```

2. In a separate terminal, start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. Open your browser and navigate to the URL shown in the Streamlit terminal output (usually http://localhost:8501)

## How It Works

1. **Data Extraction**: The system scrapes course information from Brainlox's technical courses page
2. **Knowledge Base Creation**: Text is processed, split into chunks, and stored in a vector database
3. **User Interaction**: When a user asks a question, the system:
   - Searches for the most relevant course information
   - Uses Mistral AI to generate a helpful response based on the retrieved information
   - Maintains conversation context for follow-up questions

## Project Structure

```
brainlox-chatbot/
├── .env                  # Environment variables
├── .gitignore            # Git ignore file
├── README.md             # Project documentation
├── requirements.txt      # Dependencies
├── app.py                # Streamlit app
├── api.py                # Flask RESTful API
├── scraper.py            # Web scraping module
├── embeddings.py         # Embedding creation and vector store
├── chatbot.py            # Chatbot logic
└── utils/
    ├── __init__.py
    └── helpers.py        # Helper functions
```


## Acknowledgements

- [Brainlox](https://brainlox.com) for providing valuable technical course content
- [Mistral AI](https://mistral.ai) for their powerful language models
- [LangChain](https://python.langchain.com) for the excellent framework
