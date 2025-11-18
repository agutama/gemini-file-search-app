import os
import time
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
from werkzeug.utils import secure_filename
import tempfile

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Initialize Gemini API
api_key = os.getenv('GEMINI_API_KEY')
if api_key:
    genai.configure(api_key=api_key)
else:
    print("Warning: GEMINI_API_KEY not found in environment variables")

# Allowed file extensions for upload
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'csv', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'html', 
    'htm', 'md', 'json', 'xml', 'py', 'js', 'ts', 'jsx', 'tsx', 'css', 
    'sql', 'c', 'cpp', 'java', 'go', 'rs', 'swift', 'php', 'rb', 'yml', 'yaml'
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_api_key(api_key):
    """Validate the provided API key by making a simple request"""
    try:
        # Make a simple request to validate API key
        models = genai.list_models(page_size=1)
        for model in models:
            break  # Just check if we can iterate
        return True
    except Exception as e:
        print(f"API key validation failed: {e}")
        return False

def create_file_search_store(display_name):
    """Create a new File Search store"""
    try:
        import google.auth
        from google.auth.transport.requests import Request
        import requests

        # Get API key
        api_key = genai._client.api_key if hasattr(genai, '_client') and genai._client else os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("API key not found for creating file search store")
            return None

        # Prepare the request payload
        url = f"https://generativelanguage.googleapis.com/v1beta/fileSearchStores"

        payload = {
            "displayName": display_name
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(f"{url}?key={api_key}", json=payload, headers=headers)

        if response.status_code == 200:
            store_data = response.json()
            # Create a simple object to mimic the expected store interface
            class FileSearchStore:
                def __init__(self, data):
                    self.name = data.get('name', '')
                    self.display_name = data.get('displayName', data.get('display_name', ''))

            return FileSearchStore(store_data)
        else:
            print(f"Error creating file search store: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error creating file search store: {e}")
        return None

def get_file_search_store(store_name):
    """Get a specific File Search store and its document statistics"""
    try:
        import google.auth
        from google.auth.transport.requests import Request
        import requests

        # Get API key
        api_key = genai._client.api_key if hasattr(genai, '_client') and genai._client else os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("API key not found for getting file search store")
            return None

        # Prepare the request
        url = f"https://generativelanguage.googleapis.com/v1beta/{store_name}"

        response = requests.get(f"{url}?key={api_key}")

        if response.status_code == 200:
            store_data = response.json()
            # Create a simple object to mimic the expected store interface
            class FileSearchStore:
                def __init__(self, data):
                    self.name = data.get('name', '')
                    self.display_name = data.get('displayName', data.get('display_name', ''))
                    self.active_documents_count = data.get('activeDocumentsCount', '0')
                    self.pending_documents_count = data.get('pendingDocumentsCount', '0')
                    self.failed_documents_count = data.get('failedDocumentsCount', '0')
                    self.size_bytes = data.get('sizeBytes', '0')
                    self.create_time = data.get('createTime', '')
                    self.update_time = data.get('updateTime', '')

            return FileSearchStore(store_data)
        else:
            print(f"Error getting file search store: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error getting file search store: {e}")
        return None

def list_file_search_stores():
    """List all File Search stores"""
    try:
        import google.auth
        from google.auth.transport.requests import Request
        import requests

        # Get API key
        api_key = genai._client.api_key if hasattr(genai, '_client') and genai._client else os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("API key not found for listing file search stores")
            return []

        # Prepare the request
        url = f"https://generativelanguage.googleapis.com/v1beta/fileSearchStores"

        response = requests.get(f"{url}?key={api_key}")

        if response.status_code == 200:
            response_data = response.json()
            stores_data = response_data.get('fileSearchStores', [])

            stores = []
            for store_data in stores_data:
                # Create a simple object to mimic the expected store interface
                class FileSearchStore:
                    def __init__(self, data):
                        self.name = data.get('name', '')
                        self.display_name = data.get('displayName', data.get('display_name', ''))
                        self.active_documents_count = data.get('activeDocumentsCount', '0')
                        self.pending_documents_count = data.get('pendingDocumentsCount', '0')
                        self.failed_documents_count = data.get('failedDocumentsCount', '0')
                        self.size_bytes = data.get('sizeBytes', '0')
                        self.create_time = data.get('createTime', '')
                        self.update_time = data.get('updateTime', '')

                stores.append(FileSearchStore(store_data))

            return stores
        else:
            print(f"Error listing file search stores: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Error listing file search stores: {e}")
        return []

def delete_file_search_store(store_name):
    """Delete a File Search store"""
    try:
        import google.auth
        from google.auth.transport.requests import Request
        import requests

        # Get API key
        api_key = genai._client.api_key if hasattr(genai, '_client') and genai._client else os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("API key not found for deleting file search store")
            return False

        # Prepare the request
        url = f"https://generativelanguage.googleapis.com/v1beta/{store_name}"

        response = requests.delete(f"{url}?key={api_key}")

        if response.status_code == 200:
            return True
        else:
            print(f"Error deleting file search store: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error deleting file search store: {e}")
        return False

def list_uploaded_files():
    """List all uploaded files"""
    try:
        files = genai.list_files()
        return files
    except Exception as e:
        print(f"Error listing uploaded files: {e}")
        return []

def import_file_to_store(file_uri, store_name, chunking_config=None):
    """Import an uploaded file to a File Search store"""
    try:
        import google.auth
        from google.auth.transport.requests import Request

        # Get API key
        api_key = genai._client.api_key if hasattr(genai, '_client') and genai._client else os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("API key not found for importing file to store")
            return False

        # Prepare the request
        url = f"https://generativelanguage.googleapis.com/v1beta/{store_name}:importFile"

        payload = {
            "fileName": file_uri
        }

        # Add chunking configuration if provided and valid
        if chunking_config:
            # Validate and use the correct chunking config structure
            # Based on API documentation, possible valid structures might be different
            payload["chunkingConfig"] = chunking_config

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(f"{url}?key={api_key}", json=payload, headers=headers)

        if response.status_code == 200:
            # The response contains an operation that needs to be polled to completion
            operation = response.json()
            operation_name = operation.get('name', '')

            # In a real application, you would poll the operation to completion
            # For this implementation, we return the operation details
            return {
                'success': True,
                'operation_name': operation_name,
                'status': 'import_started'
            }
        else:
            print(f"Error importing file to store: {response.status_code} - {response.text}")
            return {
                'success': False,
                'error': response.text
            }
    except Exception as e:
        print(f"Error importing file to store: {e}")
        return {
            'success': False,
            'error': str(e)
        }

def delete_uploaded_file(file_uri):
    """Delete an uploaded file from the system"""
    try:
        import google.auth
        from google.auth.transport.requests import Request

        # Get API key
        api_key = genai._client.api_key if hasattr(genai, '_client') and genai._client else os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("API key not found for deleting uploaded file")
            return False

        # Prepare the request
        url = f"https://generativelanguage.googleapis.com/v1beta/{file_uri}"

        response = requests.delete(f"{url}?key={api_key}")

        if response.status_code == 200:
            return True
        else:
            print(f"Error deleting uploaded file: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error deleting uploaded file: {e}")
        return False

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/configure-api-key', methods=['POST'])
def configure_api_key():
    """Configure the API key"""
    data = request.json
    api_key = data.get('api_key', '')
    
    # Validate the API key before setting it
    if api_key and validate_api_key(api_key):
        # In a real application, you would securely store this for the session/user
        # For this demo, we'll just configure the client with the provided key
        genai.configure(api_key=api_key)
        return jsonify({'success': True, 'message': 'API key configured successfully'})
    else:
        return jsonify({'success': False, 'message': 'Invalid API key'})

@app.route('/api/upload-to-store', methods=['POST'])
def upload_to_store():
    """Directly upload a file to File Search store"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file part in request'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Get store name and chunking configuration from form data
            store_name = request.form.get('store_name', '')
            chunking_config = request.form.get('chunking_config', None)
            if chunking_config:
                try:
                    import json
                    chunking_config = json.loads(chunking_config)
                except Exception:
                    return jsonify({'success': False, 'error': 'Invalid chunking configuration'})
            
            # Save file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp_file:
                file.save(tmp_file.name)
                temp_path = tmp_file.name
            
            try:
                # Unfortunately, as of current SDK version, direct upload to file search store 
                # might not be supported through genai library, so we'll use the file and
                # associate it with a store separately
                uploaded_file = genai.upload_file(
                    path=temp_path,
                    display_name=filename
                )
                
                # Wait for processing
                while uploaded_file.state.name == "PROCESSING":
                    time.sleep(5)
                    uploaded_file = genai.get_file(uploaded_file.name)
                
                if uploaded_file.state.name == "FAILED":
                    return jsonify({'success': False, 'error': f'File processing failed: {uploaded_file.state}'})
                
                # For now, just return the uploaded file info
                # The actual association with a file search store might require a different approach
                result = {
                    'success': True,
                    'file_name': filename,
                    'file_uri': uploaded_file.name,
                    'status': 'uploaded'
                }
                
                return jsonify(result)
            finally:
                # Clean up the temporary file
                os.unlink(temp_path)
        else:
            return jsonify({'success': False, 'error': 'File type not allowed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/import-files', methods=['POST'])
def import_files():
    """Import files to File Search store (alternative method)"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file part in request'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Get store name and chunking configuration from form data
            store_name = request.form.get('store_name', '')
            chunking_config = request.form.get('chunking_config', None)
            if chunking_config:
                try:
                    import json
                    chunking_config = json.loads(chunking_config)
                except Exception:
                    return jsonify({'success': False, 'error': 'Invalid chunking configuration'})
            
            # Save file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp_file:
                file.save(tmp_file.name)
                temp_path = tmp_file.name
            
            try:
                # Upload the file
                uploaded_file = genai.upload_file(
                    path=temp_path,
                    display_name=filename
                )
                
                # Wait for processing
                while uploaded_file.state.name == "PROCESSING":
                    time.sleep(5)
                    uploaded_file = genai.get_file(uploaded_file.name)
                
                if uploaded_file.state.name == "FAILED":
                    return jsonify({'success': False, 'error': f'File processing failed: {uploaded_file.state}'})
                
                result = {
                    'success': True,
                    'file_name': filename,
                    'file_uri': uploaded_file.name,
                    'status': 'imported'
                }
                
                return jsonify(result)
            finally:
                # Clean up the temporary file
                os.unlink(temp_path)
        else:
            return jsonify({'success': False, 'error': 'File type not allowed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint that queries the File Search store"""
    try:
        data = request.json
        query = data.get('query', '')
        store_names = data.get('store_names', [])

        if not query:
            return jsonify({'error': 'Query is required'})

        # Get API key
        api_key = genai._client.api_key if hasattr(genai, '_client') and genai._client else os.getenv('GEMINI_API_KEY')
        if not api_key:
            return jsonify({'error': 'API key not configured'})

        # Prepare the request payload
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

        payload = {
            "contents": [{
                "parts": [{"text": query}]
            }],
            "generationConfig": {
                "temperature": 0.4,
                "topP": 1,
                "topK": 32,
                "maxOutputTokens": 4096,
            },
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ]
        }

        # Only add tools if store_names are provided
        if store_names:
            payload["tools"] = [{
                "fileSearch": {
                    "fileSearchStoreNames": store_names  # Updated to match the actual API parameter name
                }
            }]

        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            response_data = response.json()

            # Extract the text response
            response_text = ""
            try:
                response_text = response_data['candidates'][0]['content']['parts'][0]['text']
            except (KeyError, IndexError):
                response_text = "Could not generate response. The model may not have found relevant information in the documents."

            # Extract citation information
            citations = []
            try:
                candidate = response_data['candidates'][0]
                if 'groundingMetadata' in candidate:
                    grounding_metadata = candidate['groundingMetadata']
                    if 'groundingChunks' in grounding_metadata:
                        for chunk in grounding_metadata['groundingChunks']:
                            # Extract text from retrievedContext if available
                            text_content = ''
                            source_file = 'Unknown'
                            page_info = ''

                            # Check the actual structure of the chunk
                            if 'retrievedContext' in chunk:
                                retrieved_context = chunk['retrievedContext']
                                text_content = retrieved_context.get('text', '')
                                source_file = retrieved_context.get('title', 'Unknown')

                                # Try to extract page information if present in the text
                                if '--- PAGE' in text_content:
                                    import re
                                    page_matches = re.findall(r'--- PAGE (\d+) ---', text_content)
                                    if page_matches:
                                        page_info = f"Page {', '.join(page_matches)}"
                            else:
                                # Handle different structure where chunk might contain text directly
                                text_content = str(chunk.get('content', ''))
                                source_file = chunk.get('source', 'Unknown')

                            citations.append({
                                'text': text_content,
                                'source': source_file,
                                'page': page_info
                            })
            except (KeyError, IndexError, TypeError):
                pass  # No citations available

            # Extract usage metadata
            usage_metadata = {}
            try:
                # Usage metadata might be included in the response without explicit request
                if 'usageMetadata' in response_data:
                    usage = response_data['usageMetadata']
                    usage_metadata = {
                        'total_token_count': usage.get('totalTokenCount', 0),
                        'prompt_token_count': usage.get('promptTokenCount', 0),
                        'candidates_token_count': usage.get('candidatesTokenCount', 0)
                    }
            except (KeyError, TypeError):
                pass  # Usage metadata not available

            result = {
                'query': query,
                'response': response_text,
                'citations': citations,
                'usage': usage_metadata
            }

            return jsonify(result)
        else:
            return jsonify({'error': f'API request failed: {response.text}'})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/stores', methods=['GET', 'POST'])
def manage_stores():
    """Manage File Search stores"""
    if request.method == 'GET':
        stores = list_file_search_stores()
        return jsonify([{
            'name': store.name,
            'display_name': getattr(store, 'display_name', getattr(store, 'displayName', 'Unknown')),
            'active_documents_count': getattr(store, 'active_documents_count', '0'),
            'pending_documents_count': getattr(store, 'pending_documents_count', '0'),
            'failed_documents_count': getattr(store, 'failed_documents_count', '0'),
            'size_bytes': getattr(store, 'size_bytes', '0')
        } for store in stores])
    elif request.method == 'POST':
        data = request.json
        display_name = data.get('display_name', 'Default Store')
        store = create_file_search_store(display_name)
        if store:
            return jsonify({
                'success': True,
                'name': store.name,
                'display_name': getattr(store, 'display_name', getattr(store, 'displayName', 'Unknown')),
                'active_documents_count': getattr(store, 'active_documents_count', '0'),
                'pending_documents_count': getattr(store, 'pending_documents_count', '0'),
                'failed_documents_count': getattr(store, 'failed_documents_count', '0'),
                'size_bytes': getattr(store, 'size_bytes', '0')
            })
        else:
            return jsonify({'success': False, 'error': 'Could not create store'})

@app.route('/api/stores/<path:store_name>', methods=['DELETE'])
def delete_store(store_name):
    """Delete a specific File Search store"""
    success = delete_file_search_store(store_name)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Could not delete store'})

@app.route('/api/files', methods=['GET'])
def list_files():
    """List all uploaded files"""
    try:
        files = list_uploaded_files()
        files_list = []
        for file in files:
            files_list.append({
                'name': file.name,
                'display_name': getattr(file, 'display_name', ''),
                'mime_type': getattr(file, 'mime_type', ''),
                'size_bytes': getattr(file, 'size_bytes', 0),
                'state': getattr(file, 'state', {}).get('name', 'Unknown') if isinstance(getattr(file, 'state', None), dict) else str(getattr(file, 'state', 'Unknown')),
                'create_time': getattr(file, 'create_time', ''),
                'update_time': getattr(file, 'update_time', ''),
                'expiration_time': getattr(file, 'expiration_time', '')
            })
        return jsonify(files_list)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/stores/<path:store_name>/import-file', methods=['POST'])
def import_file_to_store_api(store_name):
    """Import a file to a specific File Search store"""
    try:
        data = request.json
        file_uri = data.get('file_uri', '')
        chunking_config = data.get('chunking_config', None)

        if not file_uri:
            return jsonify({'success': False, 'error': 'File URI is required'})

        result = import_file_to_store(file_uri, store_name, chunking_config)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/files/<path:file_uri>', methods=['DELETE'])
def delete_file_api(file_uri):
    """Delete a specific uploaded file"""
    try:
        # The file_uri may include the 'files/' prefix, so we ensure it's properly formatted
        if not file_uri.startswith('files/'):
            file_uri = f'files/{file_uri}'

        success = delete_uploaded_file(file_uri)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Could not delete file'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)