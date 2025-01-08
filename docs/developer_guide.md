# Keboola Storage Browser - Developer Documentation

## Table of Contents
1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Setup and Installation](#setup-and-installation)
4. [Backend Architecture](#backend-architecture)
5. [Frontend Architecture](#frontend-architecture)
6. [API Endpoints](#api-endpoints)
7. [Testing](#testing)
8. [Security Considerations](#security-considerations)
9. [Contributing Guidelines](#contributing-guidelines)

## Overview

The Keboola Storage Browser is a web application that allows users to browse and explore their Keboola Storage API data. The application provides a user-friendly interface for:
- Authenticating with Keboola Storage API
- Browsing buckets and tables
- Viewing table details and metadata
- Previewing table data

### Tech Stack
- Backend: Python Flask
- Frontend: HTML, CSS, JavaScript
- Testing: pytest, responses
- API Integration: Keboola Storage API

## Project Structure

```
keboola-storage-browser/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── static/               # Frontend assets
│   └── index.html        # Main frontend interface
├── tests/                # Test suite
│   ├── conftest.py       # Test configurations and fixtures
│   └── test_app.py       # Test cases
├── venv/                 # Virtual environment
└── docs/                 # Documentation
    └── developer_guide.md # This document
```

## Setup and Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)
- Git

### Local Development Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd keboola-storage-browser
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`.

## Backend Architecture

### Core Components

#### Flask Application (`app.py`)
- Handles HTTP requests
- Manages user sessions
- Proxies requests to Keboola Storage API
- Implements security measures

### Session Management
- Uses Flask sessions to store authentication tokens
- Session data includes:
  - Keboola Storage API token
  - API endpoint URL

### Error Handling
- Comprehensive error handling for API requests
- HTTP status codes mapping
- User-friendly error messages

## Frontend Architecture

### Components

#### Main Interface (`static/index.html`)
- Login form with endpoint selection
- Bucket and table browser
- Table details modal
- Data preview functionality

### JavaScript Modules

#### Authentication
- Handles user login/logout
- Manages API token storage
- Session management

#### Data Display
- Bucket list rendering
- Table list rendering
- Table details modal
- Data preview functionality

#### API Integration
- Fetch buckets and tables
- Retrieve table details
- Load data previews

## API Endpoints

### Authentication
```
POST /api/login
Request:
{
    "token": "your-keboola-token",
    "endpoint": "connection.keboola.com"
}
Response:
{
    "message": "Login successful"
}
```

### Bucket Operations
```
GET /api/buckets
Response:
[
    {
        "id": "in.c-bucket",
        "name": "Bucket Name",
        ...
    }
]
```

### Table Operations
```
GET /api/buckets/{bucket_id}/tables
Response:
[
    {
        "id": "table_id",
        "name": "Table Name",
        ...
    }
]

GET /api/tables/{table_id}/preview
Response:
{
    "columns": ["col1", "col2"],
    "rows": [...]
}
```

## Testing

### Test Structure

#### Configuration (`tests/conftest.py`)
- Test fixtures
- Mock data
- Environment setup

#### Test Cases (`tests/test_app.py`)
- Unit tests for all endpoints
- Integration tests
- Mock API responses

### Running Tests
```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run specific test
python -m pytest -k "test_name"
```

### Test Coverage
- Authentication flows
- API endpoint functionality
- Error handling
- Session management

## Security Considerations

### API Token Handling
- Tokens stored in server-side sessions
- No token persistence in frontend
- Secure session cookie configuration

### CORS Configuration
- Restricted to necessary origins
- Proper header handling
- Security headers implementation

### Error Handling
- No sensitive data in error messages
- Proper status code usage
- Input validation

## Contributing Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use consistent JavaScript formatting
- Maintain clean HTML/CSS structure

### Pull Request Process
1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Update documentation
5. Submit pull request

### Development Workflow
1. Create feature branch
2. Implement changes
3. Write/update tests
4. Update documentation
5. Submit pull request

### Testing Requirements
- All tests must pass
- New features require tests
- Maintain test coverage
- Update test documentation 