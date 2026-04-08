#https://vita-tax-questionnaire.streamlit.app
#vita-tax-questionnaire

import os
import pickle
import streamlit as st
from fpdf import FPDF
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

from Function import ask_question
from BasicInfo import BasicInfo, HealthInsurance, CaResidency, MiscQuestions, answers
BasicInfo()

FOLDER_ID = "1X7OA9TyD7cVTYXhLrj--Z_T7mQqXu5nt"
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_drive_service():
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["google_service_account"],
        scopes=SCOPES
    )
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

if st.button("Generate PDF & Upload"):
    pdf_file = generate_pdf(answers)
    st.success(f"PDF generated: {pdf_file}")

    try:
        file_id = upload_to_drive(pdf_file)
        st.success(f"Uploaded to Google Drive!\nFile ID: {file_id}\nFolder ID: {FOLDER_ID}")
        st.balloons()
    except Exception as e:
        st.error(f"Upload failed: {e}")

