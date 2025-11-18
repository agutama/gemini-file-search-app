# Gemini File Search Demo

A web application that demonstrates the use of Google's Gemini File Search API to upload documents, index them, and query their content using a chatbot interface.

## Features

- API key configuration with validation
- File Search store management (create, list, delete)
- Direct upload to File Search store
- Import files to File Search store
- Configurable chunking settings for document processing
- Chatbot interface for querying document content
- Visual representation of the File Search indexing and querying process

## Requirements

- Python 3.8+
- Google Gemini API key

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

1. Start the application:
   ```bash
   python app.py
   ```
2. Open your browser and navigate to `http://localhost:5000`
3. Configure your API key in the API Configuration section
4. Create a File Search store
5. Upload or import documents to your store
6. Use the chat interface to ask questions about your documents

## Architecture

The application follows the File Search workflow:

1. **Create File Search Store**: A persistent container for document embeddings
2. **Index Documents**: Upload and process documents into embeddings
3. **Query with RAG**: Ask questions and get responses grounded in document content

## API Endpoints

- `POST /api/configure-api-key`: Configure the Gemini API key
- `GET/POST /api/stores`: Manage File Search stores
- `DELETE /api/stores/<store_name>`: Delete a store
- `POST /api/upload-to-store`: Directly upload a file to a store
- `POST /api/import-files`: Import a file to a store via the Files API
- `POST /api/chat`: Query documents in a store

## Supported File Types

The application supports various file formats including:
- Text files (.txt, .md)
- Documents (.pdf, .doc, .docx)
- Spreadsheets (.xls, .xlsx, .csv)
- Presentations (.ppt, .pptx)
- Code files (.py, .js, .ts, .java, etc.)
- Markup files (.html, .xml, .json)

## Chunking Configuration

Control how documents are split during indexing:
- Max Tokens per Chunk: Number of tokens in each chunk (default: 200)
- Max Overlap Tokens: Number of overlapping tokens between chunks (default: 20)

This helps optimize retrieval accuracy for different types of documents.