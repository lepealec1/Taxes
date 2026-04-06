import streamlit as st
from fpdf import FPDF
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import pickle

# ----------------------------
# Paths & OAuth setup
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.pkl")
SCOPES = ['https://www.googleapis.com/auth/drive.file']
FOLDER_ID = "1X7OA9TyD7cVTYXhLrj--Z_T7mQqXu5nt"  # Your Google Drive folder

def get_drive_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        # Headless authorization for Streamlit Cloud
        creds = flow.run_local_server(port=0, open_browser=False)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
    return build('drive', 'v3', credentials=creds)

# ----------------------------
# PDF generation
# ----------------------------
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

# ----------------------------
# Upload PDF to Drive
# ----------------------------
def upload_to_drive(file_path):
    service = get_drive_service()
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [FOLDER_ID]
    }
    media = MediaFileUpload(file_path, mimetype='application/pdf')
    uploaded_file = service.files().create(
        body=file_metadata, media_body=media, fields='id'
    ).execute()
    return uploaded_file.get('id')

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("PDF Generator + Google Drive Upload")

# --- Form Inputs ---
answers = {}
answers['name'] = st.text_input("Your name")
answers['email'] = st.text_input("Email")
answers['refund_method'] = st.selectbox("Refund Method", ["Direct Deposit", "Check by Mail"])

# --- Generate & Upload PDF ---
if st.button("Generate PDF & Upload"):
    try:
        pdf_file = generate_pdf(answers)
        st.success(f"PDF generated: {pdf_file}")

        file_id = upload_to_drive(pdf_file)
        st.success(f"Uploaded to Google Drive!\nFile ID: {file_id}\nFolder ID: {FOLDER_ID}")

        st.balloons()  # optional celebration 🎉

    except Exception as e:
        st.error(f"Upload failed: {e}")