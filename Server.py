import streamlit as st
from fpdf import FPDF
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

# --- PDF generation ---
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

# --- OAuth 2.0 Google Drive ---
SCOPES = ['https://www.googleapis.com/auth/drive.file']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, "Client_Secret.json")


def upload_to_drive(file_path, folder_id):
    # Authenticate
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=8888)
    service = build('drive', 'v3', credentials=creds)

    # Upload file into specified folder
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, mimetype='application/pdf')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

# --- Streamlit UI ---
st.title("PDF Generator + Google Drive Upload")

answers = {}
answers['name'] = st.text_input("Your name")
answers['email'] = st.text_input("Email")
answers['refund_method'] = st.selectbox("Refund Method", ["Direct Deposit", "Check by Mail"])

if st.button("Generate PDF & Upload"):
    pdf_file = generate_pdf(answers)
    st.success(f"PDF generated: {pdf_file}")
    
    folder_id = "1iajsRfYZ8c0H5bwzLB1SXiY8EkcutGjo"  # your folder ID
    file_id = upload_to_drive(pdf_file, folder_id)
    st.success(f"Uploaded to Google Drive!\nFile ID: {file_id}\nFolder ID: {folder_id}")


from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "service_account.json")

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

file_metadata = {'name': 'test.pdf', 'parents': ['your-folder-id']}
media = MediaFileUpload('test.pdf', mimetype='application/pdf')
file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

print("Uploaded file ID:", file.get('id'))