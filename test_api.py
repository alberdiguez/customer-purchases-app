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

# Test adding single purchase
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

# Test adding multiple purchases in bulk
def test_bulk_upload_purchases():
    # Prepare test data for bulk upload
    bulk_data = """customer_name,country,purchase_date,amount
Paula Vera,Spain,2024-02-20,550.0
Victoria,France,2025-02-21,150.0
"""

    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_csv:
        temp_csv.write(bulk_data.encode('utf-8'))
        temp_csv_path = temp_csv.name

    # Send POST request to /purchase/bulk/ endpoint with temporary CSV file
    with open(temp_csv_path, 'rb') as f:
        response = httpx.post(f"{url_api}/purchase/bulk/", files={"file": (temp_csv_path, f, "text/csv")})

    # Verify succesful response
    assert response.status_code == 200

    # Clean up the temporary file
    os.remove(temp_csv_path)

# Test GET request for purchases
def test_get_purchases():
    # Send GET request to /purchases/ endpoint to get purchases
    response = httpx.get(f"{url_api}/purchases/")

    # Verify if the response is successful
    assert response.status_code == 200

    # Check if the response contains purchases and if it is a list
    response_data = response.json()
    assert "purchases" in response_data
    assert isinstance(response_data["purchases"], list)

# Test invalid single purchase adding
def test_add_purchase_invalid_data():
    # Prepare invalid purchase data (missing required fields)
    invalid_data = {
        "customer_name": "",
        "country": "Spain",
        "purchase_date": "2023-02-20",
        "amount": 500.0
    }

    # Send POST request to /purchase/ endpoint with invalid purchase
    response = httpx.post(f"{url_api}/purchase/", json=invalid_data)

    # Verify that the response is not successful (should return 422 Unprocessable Entity)
    assert response.status_code == 422