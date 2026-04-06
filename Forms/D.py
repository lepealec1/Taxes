import streamlit as st
from fpdf import FPDF
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import os

# --- Streamlit Page Setup ---
st.set_page_config(layout="wide")
st.title("Supplemental Questionnaire")

# --- Collect Answers ---
answers = {}

def grid_row(key, question, options=("Yes", "No", "Unsure")):
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown(question)
    with col2:
        answers[key] = st.radio(question, options, horizontal=True, label_visibility="collapsed")

# Header
col1, col2 = st.columns([3, 1])
with col1:
    answers["name"] = st.text_input("Name")
with col2:
    answers["date"] = st.date_input("Date")

st.divider()

# Example Questions
grid_row("rent_ca_6_months", "Did you rent in California for more than 6 months of the year?")
grid_row("self_employment", "Do you have any income from self-employment?")

st.divider()

# --- Generate PDF ---
def generate_pdf(data, filename="questionnaire.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Supplemental Questionnaire", ln=True, align="C")
    pdf.set_font("Arial", '', 12)
    for key, value in data.items():
        pdf.multi_cell(0, 8, f"{key.replace('_',' ').title()}: {value}")
        pdf.ln(1)
    pdf.output(filename)
    return filename

# --- Google Drive Upload ---
# Set your folder ID here
FOLDER_ID = "1NqqjYG1kPtOEzMCH_rKB2kHLJn5EnVOe"  

# Service Account credentials (hard-coded)
SERVICE_ACCOUNT_INFO = {
    "type": "service_account",
    "project_id": "taxes-492518",
    "private_key_id": "YOUR_PRIVATE_KEY_ID",
    "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBK...
...rest of your key...
...end of your key...
-----END PRIVATE KEY-----\n""",
    "client_email": "taxes-137@taxes-492518.iam.gserviceaccount.com",
    "client_id": "YOUR_CLIENT_ID",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "YOUR_CERT_URL"
}

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def upload_to_drive(file_path):
    creds = service_account.Credentials.from_service_account_info(
        SERVICE_ACCOUNT_INFO, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [FOLDER_ID]  # Upload to specific folder
    }
    media = MediaFileUpload(file_path, mimetype='application/pdf')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

# --- Streamlit Button ---
if st.button("Generate PDF and Upload to Google Drive"):
    pdf_file = generate_pdf(answers)
    file_id = upload_to_drive(pdf_file)
    st.success(f"PDF uploaded successfully! File ID: {file_id}")