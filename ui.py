import streamlit as st
import requests

st.title("Customer Purchases App")

# Tabs
tab1, tab2 = st.tabs(["Upload Purchases", "Analyse Purchases"])

with tab1:
    # Add single Purchase form
    st.header("Add Purchase")
    customer_name = st.text_input("Customer Name")
    country = st.text_input("Country")
    purchase_date = st.date_input("Purchase Date")
    amount = st.number_input("Amount", min_value=0.0)
    if (st.button("Add Purchase")):
        # Create dictionary to hold purchase details
        purchase_data = {
            'customer_name': customer_name,
            'country': country,
            'purchase_date': purchase_date,
            'amount': amount        
        }
        # Send POST request to /purchase/
        response = requests.post("http://127.0.0.1:8000/purchase/", json=purchase_data)
        # Check API response
        if response.status_code == 200:
            st.success("Purchase added succesfully!")
        else:
            st.error("Error adding purchase.")

    # Add multiple Purchases from CSV
    st.header("Add Purchases from CSV file")
    uploaded_file = st.file_uploader("Please select a CSV file", type='csv')
    if st.button("Upload"):
        if uploaded_file is not None:
            file = {'file': uploaded_file}
            # Send POST request to /purchase/bulk/
            resposne = requests.post("http://127.0.0.1:8000/purchase/bulk/", files = file)
            # Check API response
            if resposne.status_code == 200:
                st.success("Multiple purchases added successfully!")
            else:
                st.error("Error uploading purchases.")

with tab2:
    st.header("View Purchases")
    # Filters form
    country_filter = st.text_input("Filter by Country")
    start_date_filter = st.date_input("Start Date")
    end_date_filter = st.date_input("End Date")

    if st.button("Get Purchases"):
        # Prepare query parameters
        params = {}
        if country_filter:
            params["country"] = country_filter
        if start_date_filter:
            params["start_date"] = start_date_filter.isoformat()
        if end_date_filter:
            params["end_date"] = end_date_filter.isoformat()

        # Make GET request to /purchases/
        response = requests.get("http://127.0.0.1:8000/purchases/", params=params)
        # Check API response
        if response.status_code == 200:
            purchases = response.json()
            # Display purchases if any match the given criteria
            if purchases:
                st.write(purchases)
            else:
                st.write("No purchases found for the given criteria")
        else:
            st.error("Error retrieving purchases.")