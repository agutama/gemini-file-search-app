document.addEventListener('DOMContentLoaded', function() {
    // API Configuration
    document.getElementById('save-api-key').addEventListener('click', function() {
        const apiKey = document.getElementById('api-key').value;
        fetch('/api/configure-api-key', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ api_key: apiKey })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('API key saved successfully!');
            } else {
                alert('Error saving API key: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error saving API key');
        });
    });
    
    // Store Management
    document.getElementById('create-store').addEventListener('click', function() {
        const storeName = document.getElementById('store-name').value;
        if (!storeName) {
            alert('Please enter a store name');
            return;
        }
        
        fetch('/api/stores', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ display_name: storeName })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Store created successfully!');
                listStores();
            } else {
                alert('Error creating store: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error creating store');
        });
    });
    
    document.getElementById('list-stores').addEventListener('click', listStores);
    
    // Initial load of stores
    listStores();
    
    // Direct Upload
    document.getElementById('direct-upload-btn').addEventListener('click', function() {
        const fileInput = document.getElementById('direct-upload-file');
        const storeSelect = document.getElementById('direct-upload-store');
        
        if (!fileInput.files.length) {
            alert('Please select a file to upload');
            return;
        }
        
        if (!storeSelect.value) {
            alert('Please select a store');
            return;
        }
        
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('store_name', storeSelect.value);
        
        // Add chunking config
        const maxTokens = document.getElementById('max-tokens').value;
        const overlapTokens = document.getElementById('overlap-tokens').value;
        const chunkingConfig = {
            "chunkingConfig": {
                "staticChunkingConfig": {
                    "maxChunkSizeTokens": parseInt(maxTokens),
                    "overlapSizeTokens": parseInt(overlapTokens)
                }
            }
        };
        formData.append('chunking_config', JSON.stringify(chunkingConfig));
        
        fetch('/api/upload-to-store', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('File uploaded successfully!');
            } else {
                alert('Error uploading file: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error uploading file');
        });
    });
    
    // Import Files
    document.getElementById('import-btn').addEventListener('click', function() {
        const fileInput = document.getElementById('import-file');
        const storeSelect = document.getElementById('import-store');
        
        if (!fileInput.files.length) {
            alert('Please select a file to import');
            return;
        }
        
        if (!storeSelect.value) {
            alert('Please select a store');
            return;
        }
        
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('store_name', storeSelect.value);
        
        // Add chunking config
        const maxTokens = document.getElementById('max-tokens').value;
        const overlapTokens = document.getElementById('overlap-tokens').value;
        const chunkingConfig = {
            "chunkingConfig": {
                "staticChunkingConfig": {
                    "maxChunkSizeTokens": parseInt(maxTokens),
                    "overlapSizeTokens": parseInt(overlapTokens)
                }
            }
        };
        formData.append('chunking_config', JSON.stringify(chunkingConfig));
        
        fetch('/api/import-files', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('File imported successfully!');
            } else {
                alert('Error importing file: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error importing file');
        });
    });
    
    // Chat functionality
    document.getElementById('send-btn').addEventListener('click', sendMessage);
    document.getElementById('chat-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    function listStores() {
        fetch('/api/stores')
        .then(response => response.json())
        .then(stores => {
            const storesList = document.getElementById('stores-list');
            const directUploadStore = document.getElementById('direct-upload-store');
            const importStore = document.getElementById('import-store-select');  // Use the correct ID
            const queryStore = document.getElementById('query-store');

            // Clear existing options
            directUploadStore.innerHTML = '<option value="">Select a store</option>';
            importStore.innerHTML = '<option value="">Select a store</option>';
            queryStore.innerHTML = '<option value="">Select a store</option>';

            storesList.innerHTML = '';

            stores.forEach(store => {
                // Add to stores list display
                const div = document.createElement('div');
                div.className = 'store-item';
                div.innerHTML = `
                    <span>${store.displayName || store.display_name} (${store.name})</span>
                    <button class="delete-store-btn" data-store-name="${store.name}">Delete</button>
                `;
                storesList.appendChild(div);

                // Add to dropdowns
                const option1 = document.createElement('option');
                option1.value = store.name;
                option1.textContent = store.displayName || store.display_name;
                directUploadStore.appendChild(option1);

                const option2 = document.createElement('option');
                option2.value = store.name;
                option2.textContent = store.displayName || store.display_name;
                importStore.appendChild(option2);  // Use importStore instead

                const option3 = document.createElement('option');
                option3.value = store.name;
                option3.textContent = store.displayName || store.display_name;
                queryStore.appendChild(option3);
            });

            // Add event listeners to delete buttons
            document.querySelectorAll('.delete-store-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const storeName = this.getAttribute('data-store-name');
                    if (confirm('Are you sure you want to delete this store?')) {
                        fetch(`/api/stores/${storeName}`, {
                            method: 'DELETE'
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                alert('Store deleted successfully!');
                                listStores(); // Refresh the list
                            } else {
                                alert('Error deleting store: ' + data.error);
                            }
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            alert('Error deleting store');
                        });
                    }
                });
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // List uploaded files
    document.getElementById('list-files').addEventListener('click', listUploadedFiles);

    function listUploadedFiles() {
        fetch('/api/files')
        .then(response => response.json())
        .then(files => {
            const filesList = document.getElementById('files-list');
            filesList.innerHTML = '';

            if (files.length === 0) {
                filesList.innerHTML = '<p>No uploaded files found.</p>';
                return;
            }

            const filesContainer = document.createElement('div');
            filesContainer.className = 'files-container';

            files.forEach(file => {
                const fileDiv = document.createElement('div');
                fileDiv.className = 'file-item';
                fileDiv.innerHTML = `
                    <div class="file-info">
                        <h4>${file.display_name || file.name}</h4>
                        <p><strong>URI:</strong> ${file.name}</p>
                        <p><strong>MIME Type:</strong> ${file.mime_type || 'Unknown'}</p>
                        <p><strong>Size:</strong> ${formatFileSize(file.size_bytes || 0)}</p>
                        <p><strong>Status:</strong> ${file.state || 'Unknown'}</p>
                        <p><strong>Created:</strong> ${file.create_time ? new Date(file.create_time).toLocaleString() : 'Unknown'}</p>
                    </div>
                `;
                filesContainer.appendChild(fileDiv);
            });

            filesList.appendChild(filesContainer);
        })
        .catch(error => {
            console.error('Error:', error);
            const filesList = document.getElementById('files-list');
            filesList.innerHTML = '<p>Error loading files list.</p>';
        });
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Enhanced file listing to include import functionality
    function listUploadedFiles() {
        fetch('/api/files')
        .then(response => response.json())
        .then(files => {
            const filesList = document.getElementById('files-list');
            const importFileSelect = document.getElementById('import-file-select');

            // Clear existing options in the import file select
            importFileSelect.innerHTML = '<option value="">Select a file</option>';

            filesList.innerHTML = '';

            if (files.length === 0) {
                filesList.innerHTML = '<p>No uploaded files found.</p>';
                return;
            }

            const filesContainer = document.createElement('div');
            filesContainer.className = 'files-container';

            files.forEach(file => {
                const fileDiv = document.createElement('div');
                fileDiv.className = 'file-item';
                fileDiv.innerHTML = `
                    <div class="file-info">
                        <h4>${file.display_name || file.name}</h4>
                        <p><strong>URI:</strong> ${file.name}</p>
                        <p><strong>MIME Type:</strong> ${file.mime_type || 'Unknown'}</p>
                        <p><strong>Size:</strong> ${formatFileSize(file.size_bytes || 0)}</p>
                        <p><strong>Status:</strong> ${file.state || 'Unknown'}</p>
                        <p><strong>Created:</strong> ${file.create_time ? new Date(file.create_time).toLocaleString() : 'Unknown'}</p>
                        <button class="import-to-store-btn" data-file-uri="${file.name}">Import to Store</button>
                        <button class="delete-file-btn" data-file-uri="${file.name}">Delete File</button>
                    </div>
                `;
                filesContainer.appendChild(fileDiv);

                // Add file to import select
                const option = document.createElement('option');
                option.value = file.name;
                option.textContent = file.display_name || file.name;
                importFileSelect.appendChild(option);
            });

            filesList.appendChild(filesContainer);

            // Show the import section and add event listeners to import buttons
            document.getElementById('import-to-store-section').style.display = 'block';

            // Add event listeners to the import buttons
            document.querySelectorAll('.import-to-store-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const fileUri = this.getAttribute('data-file-uri');
                    // Set the file URI in the import select
                    document.getElementById('import-file-select').value = fileUri;
                    // Scroll to the import section
                    document.getElementById('import-to-store-section').scrollIntoView({ behavior: 'smooth' });
                });
            });

            // Add event listeners to the delete buttons
            document.querySelectorAll('.delete-file-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const fileUri = this.getAttribute('data-file-uri');
                    if (confirm(`Are you sure you want to delete the file: ${fileUri}?`)) {
                        fetch(`/api/files/${encodeURIComponent(fileUri)}`, {
                            method: 'DELETE'
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                alert('File deleted successfully!');
                                // Refresh the file list
                                listUploadedFiles();
                            } else {
                                alert('Error deleting file: ' + (data.error || 'Unknown error'));
                            }
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            alert('Error deleting file');
                        });
                    }
                });
            });
        })
        .catch(error => {
            console.error('Error:', error);
            const filesList = document.getElementById('files-list');
            filesList.innerHTML = '<p>Error loading files list.</p>';
        });
    }

    // Import file to store functionality
    document.getElementById('import-file-btn').addEventListener('click', function() {
        const fileUri = document.getElementById('import-file-select').value;
        const storeName = document.getElementById('import-store-select').value;

        if (!fileUri) {
            alert('Please select a file to import');
            return;
        }

        if (!storeName) {
            alert('Please select a store');
            return;
        }

        // Make API call to import file to store
        fetch(`/api/stores/${encodeURIComponent(storeName)}/import-file`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                file_uri: fileUri
                // Note: chunking_config is not being sent since it caused errors
                // The API will use default chunking configuration
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('File import started successfully! It may take a few minutes depending on the file size.');
                console.log('Import operation:', data);
            } else {
                alert('Error importing file: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error importing file');
        });
    });

    function sendMessage() {
        const input = document.getElementById('chat-input');
        const queryStore = document.getElementById('query-store');
        const message = input.value.trim();

        if (!message) {
            alert('Please enter a message');
            return;
        }

        if (!queryStore.value) {
            alert('Please select a store');
            return;
        }

        // Record start time for response time calculation
        const startTime = Date.now();

        // Add user message to chat
        addToChat('user', message);
        input.value = '';

        // Send to API
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: message,
                store_names: [queryStore.value]  // Changed to store_names array to match backend
            })
        })
        .then(response => response.json())
        .then(data => {
            // Calculate response time
            const responseTime = Date.now() - startTime;
            const responseTimeFormatted = responseTime >= 1000 ?
                `${(responseTime / 1000).toFixed(2)} seconds` :
                `${responseTime} ms`;

            if (data.response) {
                addToChat('bot', data.response);

                // Display citations in the dedicated citations section below token usage
                if (data.citations && data.citations.length > 0) {
                    let citationsHtml = `<details><summary><strong>Citations (${data.citations.length} references used)</strong></summary>`;
                    data.citations.forEach((citation, index) => {
                        citationsHtml += `
                        <div class="citation-item">
                            <p><strong>Reference ${index + 1}:</strong></p>
                            <p><strong>File ID:</strong> ${citation.source || 'Unknown'}</p>
                            <p><strong>Page:</strong> ${citation.page || 'Not specified'}</p>
                            <p><strong>Text:</strong> "${citation.text ? citation.text.substring(0, 200) + (citation.text.length > 200 ? '...' : '') : 'N/A'}"</p>
                            <hr>
                        </div>`;
                    });
                    citationsHtml += `</details>`;
                    document.getElementById('citations-display').innerHTML = citationsHtml;
                } else {
                    document.getElementById('citations-display').innerHTML = '';
                }

                // Display token usage information if available in a separate section
                if (data.usage) {
                    const usageInfo = `
                        <strong>Token Usage:</strong><br>
                        Total Token yang Digunakan: ${data.usage.total_token_count || 0}<br>
                        Token Prompt (termasuk PDF): ${data.usage.prompt_token_count || 0}<br>
                        Token Respons yang Dihasilkan: ${data.usage.candidates_token_count || 0}
                    `;
                    document.getElementById('token-usage-display').innerHTML = usageInfo;
                }

                // Display response time in the token usage section as well
                const existingTokenUsage = document.getElementById('token-usage-display').innerHTML;
                document.getElementById('token-usage-display').innerHTML = existingTokenUsage +
                    (existingTokenUsage ? '<br><br>' : '') +
                    `<strong>Response Time:</strong><br>Time taken: ${responseTimeFormatted}`;
            } else {
                addToChat('bot', 'Sorry, there was an error processing your request: ' + (data.error || 'Unknown error'));
                // Clear token usage if there was an error
                document.getElementById('token-usage-display').innerHTML =
                    `<strong>Response Time:</strong><br>Time taken: ${responseTimeFormatted}`;
            }
        })
        .catch(error => {
            // Calculate response time even for errors
            const responseTime = Date.now() - startTime;
            const responseTimeFormatted = responseTime >= 1000 ?
                `${(responseTime / 1000).toFixed(2)} seconds` :
                `${responseTime} ms`;

            console.error('Error:', error);
            addToChat('bot', 'Sorry, there was an error connecting to the API.');
            // Show response time even for errors
            document.getElementById('token-usage-display').innerHTML =
                `<strong>Response Time:</strong><br>Time taken: ${responseTimeFormatted}`;
        });
    }

    function addToChat(sender, message) {
        const chatHistory = document.getElementById('chat-history');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        // Check if the message is a valid JSON string
        try {
            const parsed = JSON.parse(message);
            // If it's valid JSON, format it properly and add as pre-formatted code
            const preElement = document.createElement('pre');
            preElement.textContent = JSON.stringify(parsed, null, 2);
            messageDiv.appendChild(preElement);
        } catch (e) {
            // If it's not valid JSON, display as plain text
            messageDiv.textContent = message;
        }

        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
});