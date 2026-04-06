import streamlit as st
from fpdf import FPDF
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import os
import json

# ---------------- PDF Generation ----------------
def generate_pdf(answers_dict, filename="questionnaire.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Supplemental Questionnaire", ln=True, align="C")
    pdf.set_font("Arial", '', 12)
    for key, value in answers_dict.items():
        if isinstance(value, list):
            value = ", ".join(map(str, value))
        pdf.multi_cell(0, 8, f"{key.replace('_',' ').title()}: {value}")
        pdf.ln(1)
    pdf.output(filename)
    return filename

# ---------------- Google Drive Upload ----------------
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def upload_to_drive(file_path, creds, folder_id):
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, mimetype='application/pdf')
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    return uploaded_file.get('id')

# ---------------- Streamlit UI ----------------
st.title("PDF Generator + Google Drive Upload")

# --- Service Account Input ---
use_local_file = st.checkbox("Use local service_account.json file?", value=True)
creds = None

if use_local_file:
    # Assume service_account.json is in same folder as script
    SERVICE_ACCOUNT_FILE = "service_account.json"
    if os.path.exists(SERVICE_ACCOUNT_FILE):
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    else:
        st.warning("Local service_account.json not found. Upload below or place in app folder.")
else:
    uploaded_file = st.file_uploader("Upload Service Account JSON", type="json")
    if uploaded_file:
        info = json.load(uploaded_file)  # parse JSON into dict
        creds = Credentials.from_service_account_info(info, scopes=SCOPES)

# --- Form Inputs ---
answers = {}
answers['name'] = st.text_input("Your name")
answers['email'] = st.text_input("Email")
answers['refund_method'] = st.selectbox("Refund Method", ["Direct Deposit", "Check by Mail"])

# --- Generate & Upload PDF ---
if st.button("Generate PDF & Upload"):
    if creds is None:
        st.error("Google credentials not set. Upload JSON or enable local file.")
    else:
        try:
            pdf_file = generate_pdf(answers)
            st.success(f"PDF generated: {pdf_file}")
            
            folder_id = "1X7OA9TyD7cVTYXhLrj--Z_T7mQqXu5nt"  # replace with your Drive folder ID
            file_id = upload_to_drive(pdf_file, creds, folder_id)
            st.success(f"Uploaded to Google Drive!\nFile ID: {file_id}\nFolder ID: {folder_id}")
        except Exception as e:
            st.error(f"Upload failed: {e}")