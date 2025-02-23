import pytest
import httpx
import tempfile
import os

url_api = "http://127.0.0.1:8000"

# Test if API is running
def test_api_running():
    # Send GET request to /purchases/ endpoint
    response = httpx.get(f"{url_api}/purchases/")
    # Verify succesful reponse
    assert response.status_code == 200

def test_add_purchase():
    # Prepare test data for single upload
    purchase_data = {
        "customer_name": "Alberto Rodriguez",
        "country": "Spain",
        "purchase_date": "2025-02-23",
        "amount": 500.0
    }
    # Send POST request to /purchase/ endpoint
    response = httpx.post(f"{url_api}/purchase/", json=purchase_data)
    
    # Verify succesful response
    assert response.status_code == 200
    
    # Verify if the purchase was added
    response_data = response.json()
    assert response_data["customer_name"] == purchase_data["customer_name"]
    assert response_data["country"] == purchase_data["country"]
    assert response_data["amount"] == purchase_data["amount"]