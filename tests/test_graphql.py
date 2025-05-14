from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)

def test_hello_query():
    """Test the hello query returns the expected greeting"""
    query = """
    {
        hello
    }
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    json_response = response.json()
    assert "errors" not in json_response
    assert json_response["data"]["hello"] == "Hello World"

def test_bye_query():
    """Test the bye query returns the expected message"""
    query = """
    {
        bye
    }
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    json_response = response.json()
    assert "errors" not in json_response
    assert json_response["data"]["bye"] == "Bye!"

def test_thousand_mutation():
    """Test the thousand mutation correctly multiplies the input"""
    query = """
    mutation {
        thousand(number: 5)
    }
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    json_response = response.json()
    assert "errors" not in json_response
    assert json_response["data"]["thousand"] == 5000
    
    # Test with another number
    query = """
    mutation {
        thousand(number: 10)
    }
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["data"]["thousand"] == 10000