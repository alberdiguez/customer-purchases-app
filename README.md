# Customer Purchases API & Streamlit App

## Project Description

This project consists of a FastAPI-based backend for managing customer purchases and a Streamlit frontend to interact with it. Both containerized using docker.

## Features

### **Backend (FastAPI)**

- Stores purchase data in-memory.
- Provides endpoints to:
  - Add a single purchase (`POST /purchase/`).
  - Upload multiple purchases via CSV (`POST /purchase/bulk/`).
  - Retrieve purchases filtered by date and country (`GET /purchases/`).
  - Compute KPIs:
    - Average purchases per client.
    - Clients per country.

### **Frontend (Streamlit)**

- User-friendly interface with two tabs:
  - Upload Tab: Allows users to add purchases manually or upload a CSV file.
  - Analysis Tab: Filters purchases by country and date range. Displays KPIs.

### **Dockerization**
- Both the backend and frontend are containerized.
- A `docker-compose.yml` file is provided for easy setup.

## Installation

### **Requirements**

- [**Docker**](https://www.docker.com/products/docker-desktop/) installed in your system.

### **Run the application**

1. **Clone this repository:**
   `git clone https://github.com/alberdiguez/customer-purchases-app`

2. **Build and start the app:**
   ```bash
   docker-compose up --build test
   ```

3. **Access the frontend at:** 
   http://localhost:8501/

4. **The backend API is available at:** 
   http://localhost:8000/docs

###**Unit Testing**
- Unit tests are implemented to ensure the functionality of the backend API endpoints. They verify that the API behaves as expected for various scenarios, including valid and invalid inputs.
- **Run Unit Tests:** 
   To run unit testing, execute the following command:
   ```bash
   docker-compose up --build test
   ```

Sample purchases CSV included for an easier testing.

Thank you!