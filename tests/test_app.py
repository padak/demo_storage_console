import json
import pytest
import responses

def test_index_returns_html(client):
    """Test that the index route returns HTML"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'

def test_login_requires_token_and_endpoint(client):
    """Test that login endpoint requires both token and endpoint"""
    response = client.post('/api/login', json={})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'Token and endpoint are required'

@responses.activate
def test_successful_login(client, mock_keboola_token, mock_keboola_endpoint):
    """Test successful login with valid credentials"""
    # Mock the Keboola API response
    responses.add(
        responses.GET,
        f'https://{mock_keboola_endpoint}/v2/storage/buckets',
        json=[],
        status=200
    )

    response = client.post('/api/login', json={
        'token': mock_keboola_token,
        'endpoint': mock_keboola_endpoint
    })

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Login successful'

@responses.activate
def test_failed_login(client, mock_keboola_token, mock_keboola_endpoint):
    """Test login failure with invalid credentials"""
    # Mock the Keboola API response for failure
    responses.add(
        responses.GET,
        f'https://{mock_keboola_endpoint}/v2/storage/buckets',
        json={'error': 'Invalid credentials'},
        status=401
    )

    response = client.post('/api/login', json={
        'token': mock_keboola_token,
        'endpoint': mock_keboola_endpoint
    })

    assert response.status_code == 401

def test_buckets_requires_auth(client):
    """Test that buckets endpoint requires authentication"""
    response = client.get('/api/buckets')
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['error'] == 'Not authenticated'

@responses.activate
def test_list_buckets(client, mock_keboola_token, mock_keboola_endpoint):
    """Test listing buckets with valid session"""
    # Mock the session
    with client.session_transaction() as session:
        session['token'] = mock_keboola_token
        session['endpoint'] = mock_keboola_endpoint

    # Mock the Keboola API response
    mock_buckets = [
        {'id': 'in.c-test', 'name': 'test bucket'},
        {'id': 'out.c-test', 'name': 'output bucket'}
    ]
    responses.add(
        responses.GET,
        f'https://{mock_keboola_endpoint}/v2/storage/buckets',
        json=mock_buckets,
        status=200
    )

    response = client.get('/api/buckets')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['id'] == 'in.c-test'

@responses.activate
def test_list_tables(client, mock_keboola_token, mock_keboola_endpoint):
    """Test listing tables in a bucket"""
    bucket_id = 'in.c-test'
    # Mock the session
    with client.session_transaction() as session:
        session['token'] = mock_keboola_token
        session['endpoint'] = mock_keboola_endpoint

    # Mock the Keboola API response
    mock_tables = [
        {'id': f'{bucket_id}.table1', 'name': 'Table 1'},
        {'id': f'{bucket_id}.table2', 'name': 'Table 2'}
    ]
    responses.add(
        responses.GET,
        f'https://{mock_keboola_endpoint}/v2/storage/buckets/{bucket_id}/tables',
        json=mock_tables,
        status=200
    )

    response = client.get(f'/api/buckets/{bucket_id}/tables')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['name'] == 'Table 1'

@responses.activate
def test_get_table_details(client, mock_keboola_token, mock_keboola_endpoint):
    """Test getting table details"""
    table_id = 'in.c-test.table1'
    # Mock the session
    with client.session_transaction() as session:
        session['token'] = mock_keboola_token
        session['endpoint'] = mock_keboola_endpoint

    # Mock the Keboola API response
    mock_table_details = {
        'id': table_id,
        'name': 'Table 1',
        'rowsCount': 100,
        'dataSizeBytes': 1024,
        'primaryKey': ['id'],
        'created': '2023-01-01T00:00:00Z',
        'lastImportDate': '2023-01-02T00:00:00Z'
    }
    responses.add(
        responses.GET,
        f'https://{mock_keboola_endpoint}/v2/storage/tables/{table_id}',
        json=mock_table_details,
        status=200
    )

    response = client.get(f'/api/buckets/in.c-test/tables/{table_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == table_id
    assert data['rowsCount'] == 100

@responses.activate
def test_get_table_preview(client, mock_keboola_token, mock_keboola_endpoint):
    """Test getting table data preview"""
    table_id = 'in.c-test.table1'
    # Mock the session
    with client.session_transaction() as session:
        session['token'] = mock_keboola_token
        session['endpoint'] = mock_keboola_endpoint

    # Mock the Keboola API response
    mock_preview_data = {
        'columns': ['id', 'name'],
        'rows': [
            [
                {'columnName': 'id', 'value': '1', 'isTruncated': False},
                {'columnName': 'name', 'value': 'Test', 'isTruncated': False}
            ]
        ]
    }
    responses.add(
        responses.GET,
        f'https://{mock_keboola_endpoint}/v2/storage/tables/{table_id}/data-preview',
        json=mock_preview_data,
        status=200
    )

    response = client.get(f'/api/tables/{table_id}/preview')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'columns' in data
    assert 'rows' in data
    assert len(data['columns']) == 2
    assert len(data['rows']) == 1 