from flask import Flask, request, jsonify, session
from flask_cors import CORS
import requests
import os
from datetime import timedelta

app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)  # for session management
app.permanent_session_lifetime = timedelta(hours=1)  # session expires after 1 hour
CORS(app, supports_credentials=True)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/session/check', methods=['GET'])
def check_session():
    if 'token' not in session or 'endpoint' not in session:
        return jsonify({'valid': False}), 401
    return jsonify({'valid': True})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    token = data.get('token')
    endpoint = data.get('endpoint')
    
    if not token or not endpoint:
        return jsonify({'error': 'Token and endpoint are required'}), 400
    
    # Test the credentials by trying to list buckets
    headers = {'X-StorageApi-Token': token}
    try:
        response = requests.get(f'https://{endpoint}/v2/storage/buckets', headers=headers)
        response.raise_for_status()
        
        # Make session permanent and store credentials
        session.permanent = True
        session['token'] = token
        session['endpoint'] = endpoint
        
        return jsonify({'message': 'Login successful'})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 401

@app.route('/api/login', methods=['DELETE'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/buckets', methods=['GET'])
def list_buckets():
    if 'token' not in session or 'endpoint' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    headers = {'X-StorageApi-Token': session['token']}
    try:
        response = requests.get(
            f'https://{session["endpoint"]}/v2/storage/buckets',
            headers=headers
        )
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/buckets/<bucket_id>/tables', methods=['GET'])
def list_tables(bucket_id):
    if 'token' not in session or 'endpoint' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    headers = {'X-StorageApi-Token': session['token']}
    try:
        response = requests.get(
            f'https://{session["endpoint"]}/v2/storage/buckets/{bucket_id}/tables',
            headers=headers
        )
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/buckets/<bucket_id>/tables/<table_id>', methods=['GET'])
def get_table_details(bucket_id, table_id):
    if 'token' not in session or 'endpoint' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    headers = {'X-StorageApi-Token': session['token']}
    try:
        response = requests.get(
            f'https://{session["endpoint"]}/v2/storage/tables/{table_id}',
            headers=headers
        )
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tables/<table_id>/preview', methods=['GET'])
def get_table_preview(table_id):
    if 'token' not in session or 'endpoint' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    headers = {
        'X-StorageApi-Token': session['token']
    }
    try:
        # Construct the URL - fixed to use data-preview
        url = f'https://{session["endpoint"]}/v2/storage/tables/{table_id}/data-preview'
        params = {
            'limit': 10,
            'format': 'json'
        }
        
        print(f"Making API call to: {url}")
        print(f"With params: {params}")
        print(f"With headers: {headers}")
        
        # Get the preview data
        preview_response = requests.get(
            url,
            headers=headers,
            params=params
        )
        
        print(f"Response status: {preview_response.status_code}")
        print(f"Response text: {preview_response.text[:1000]}")  # Print first 1000 chars of response
        
        preview_response.raise_for_status()
        return jsonify(preview_response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error in preview request: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 