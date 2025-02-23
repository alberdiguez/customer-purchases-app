import streamlit as st
import requests
import pandas as pd

st.title("Customer Purchases App")

# Organize app in 2 different tabs
tab1, tab2 = st.tabs(["Upload Purchases", "Analyse Purchases"])

with tab1:
    # Add single Purchase form
    st.header("Add Purchase")
    customer_name = st.text_input("Customer Name", placeholder="Please enter a customer name")
    country = st.text_input("Country", placeholder="Please enter a country")
    purchase_date = st.date_input("Purchase Date")
    amount = st.number_input("Amount", min_value=0.0)

    # Check if any field is empty
    disable_button = not (customer_name and country and purchase_date and amount)
    # Button disabled if there are empty fields. Warns user to fill every field
    if st.button("Add Purchase", disabled=disable_button, help="All fields must be filled"):

        # Create dictionary to hold purchase details
        purchase_data = {
            'customer_name': customer_name,
            'country': country,
            'purchase_date': purchase_date.isoformat(),
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
    # File uploader for CSV type files
    uploaded_file = st.file_uploader("Please select a CSV file", type='csv')

    if st.button("Upload"):
        if uploaded_file is not None:
            # Need to specify file name, content, and type
            file = {'file': (uploaded_file.name, uploaded_file, "text/csv")}
            # Send POST request to /purchase/bulk/
            response = requests.post("http://127.0.0.1:8000/purchase/bulk/", files = file)
            # Check API response
            if response.status_code == 200:
                st.success("Multiple purchases added successfully!")
            else:
                st.error("Error uploading purchases.")
        else:
            st.error("Please select a file.")   # Display error if no file has been selected

with tab2:
    # Filters form
    st.subheader("Filters")
    # Organize filters in 3 columns
    col1, col2, col3 = st.columns(3)

    with col1:
        country_filter = st.text_input("Country")
    with col2:
        start_date_filter = st.date_input("Start Date")
    with col3:
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
            # Parse the JSON response
            result = response.json()
            purchases = result.get("purchases", [])
            kpis = result.get("kpis", None)
            # Display purchases if any match the given criteria
            if purchases:
                st.header("Purchases")
                df = pd.DataFrame(purchases)
                # Rename columns
                df.rename(columns={
                    'customer_name': 'Customer Name',
                    'country': 'Country',
                    'purchase_date': 'Purchase Date',
                    'amount': 'Amount'
                }, inplace=True)
                # Show the DataFrame in Streamlit
                st.dataframe(df)
            else:
                st.write("No purchases found for the given criteria")
            # Display KPIs if avaliable
            if kpis:
                st.header("KPIs")
                st.subheader(f":red-background[**Mean Purchases per Client:**] {kpis['avg_purchases_per_client']:.2f}")
                st.subheader(":red-background[**Clients per Country**]")
                # Prepare data for clients per country
                clients_per_country = kpis['clients_per_country']
                # Create dataframe for clients_per_country KPI
                clients_df = pd.DataFrame(list(clients_per_country.items()), columns=['Country', 'Number of Clients'])
                st.bar_chart(clients_df.set_index('Country'))
        else:
            st.error("Error retrieving purchases.")