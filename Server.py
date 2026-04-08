from fpdf import FPDF
import os
import pickle
import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

TOKEN_FILE = "token.pkl"
SCOPES = ['https://www.googleapis.com/auth/drive.file']
FOLDER_ID = "1X7OA9TyD7cVTYXhLrj--Z_T7mQqXu5nt"  # Your folder in My Drive

def get_drive_service():
    creds = None

    # Load saved token if it exists
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    # If no valid credentials, run OAuth
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_config(
            {
                "web": {
                    "client_id": st.secrets["google_oauth"]["client_id"],
                    "client_secret": st.secrets["google_oauth"]["client_secret"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost"]
                }
            },
            scopes=SCOPES
        )

        creds = flow.run_local_server(port=0)  # automatic browser-based OAuth

        # Save token for future use
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return build('drive', 'v3', credentials=creds)

def upload_to_drive(file_path):
    service = get_drive_service()
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [FOLDER_ID]
    }
    media = MediaFileUpload(file_path, mimetype='application/pdf')
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    return uploaded_file.get('id')


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


from Function import ask_question
from BasicInfo import BasicInfo, HealthInsurance, CaResidency, MiscQuestions, answers
BasicInfo()


if st.button("Generate PDF & Upload"):
    pdf_file = generate_pdf(answers)
    st.success(f"PDF generated: {pdf_file}")

    try:
        file_id = upload_to_drive(pdf_file)
        st.success(f"Uploaded to Google Drive!\nFile ID: {file_id}\nFolder ID: {FOLDER_ID}")
        st.balloons()
    except Exception as e:
        st.error(f"Upload failed: {e}")
