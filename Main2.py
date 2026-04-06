# python3 -m streamlit run /Users/bobk/Documents/hello.py
# app.py
from Forms.W2 import run_w2
from Output.Test2 import list_pdf_fields
import streamlit as st
pdf_path = "/Users/bobk/TaxProject/1040_2025.pdf"
list_pdf_fields(pdf_path)