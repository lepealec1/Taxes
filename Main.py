# python3 -m streamlit run /Users/bobk/Documents/hello.py
# app.py
from Forms.W2 import run_w2
from Output.F1040 import run_f1040
import streamlit as st
run_f1040("/Users/bobk/TaxProject/1040_2025_filled.pdf")

st.title("Tax App")
st.write("Streamlit is working!")


# Ask user for their name
name = st.text_input("Enter your name:")

if name:
    st.write(f"Hello {name}!")

tax_year= st.number_input("Enter Tax Year", min_value=2000, max_value=2050, value=2025)

filing_status = st.selectbox("Enter Filing Status", ["Single", "Head Of Household", "Married Filing Jointly"])
st.write(f"You selected: {filing_status}")

date = st.date_input("Pick a date")
st.write(f"You selected: {date}")
st.title("Tax Calculator with W-2 Entry")

run_w2()
# Example usage:
pdf_path = "/Users/bobk/TaxProject/1040_2025.pdf"
list_pdf_fields(pdf_path)
#run_f1040("/Users/bobk/TaxProject/1040_2025.pdf")
