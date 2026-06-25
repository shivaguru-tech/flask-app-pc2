import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_status(client):
    """Test home route returns 200"""
    response = client.get('/')
    assert response.status_code == 200
    print("✅ PC2 home route returns 200")

def test_health_check(client):
    """Test health returns healthy"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    print("✅ PC2 health check passed!")

def test_add_numbers(client):
    """Test add route"""
    response = client.get('/add/5/3')
    assert response.status_code == 200
    data = response.get_json()
    assert data['result'] == 8
    print("✅ PC2 add route passed!")

def test_version_info(client):
    """Test version returns required fields"""
    response = client.get('/version')
    assert response.status_code == 200
    data = response.get_json()
    assert 'version' in data
    assert 'build' in data
    assert 'server' in data
    print("✅ PC2 version route passed!")

def test_dashboard(client):
    """Test dashboard returns pipeline info"""
    response = client.get('/dashboard')
    assert response.status_code == 200
    data = response.get_json()
    assert 'server' in data
    assert 'pipeline' in data
    assert 'endpoints' in data
    print("✅ PC2 dashboard route passed!")
