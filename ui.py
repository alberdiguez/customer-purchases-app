import streamlit as st
import requests

st.title("Customer Purchases App")

# Add single Purchase form
st.header("Add Purchase")
customer_name = st.text_input("Customer Name")
country = st.text_input("Country")
purchase_date = st.date_input("Purchase Date")
amount = st.number_input("Amount", min_value=0.0)
if (st.button("Add Purchase")):
    purchase_data = {
        'customer_name': customer_name,
        'country': country,
        'purchase_date': purchase_date,
        'amount': amount        
    }
    response = requests.post("http://127.0.0.1:8000/purchase/", json=purchase_data)
    if response.status_code == 200:
        st.success("Purchase added succesfully!")
    else:
        st.error("Error adding purchase.")

# Add Purchases from CSV
st.header("Add Purchases from CSV file")
uploaded_file = st.file_uploader("Please select a CSV file", type='csv')
if st.button("Upload"):
    if uploaded_file is not None:
        file = {'file': uploaded_file}
        respone = requests.post("http://127.0.0.1:8000/purchase/bulk/", files = file)
        if respone.status_code == 200:
            st.success("Multiple purchases added successfully!")
        else:
            st.error("Error uploading purchases.")