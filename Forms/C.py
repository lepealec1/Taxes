from fpdf import FPDF
import os

# Directory of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

pdf_file = os.path.join(BASE_DIR, "test.pdf")  # full path

answers = {
    "name": "Alice",
    "date": "2026-04-06",
    "health_status": "All Year",
    "1095_a": True,
    "1095_b": False
}

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", 'B', 16)
pdf.cell(0, 10, "Supplemental Questionnaire", ln=True, align="C")
pdf.set_font("Arial", '', 12)
for key, value in answers.items():
    pdf.multi_cell(0, 8, f"{key.replace('_',' ').title()}: {value}")
    pdf.ln(1)
pdf.output(pdf_file)
print("PDF generated at:", pdf_file)

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'Service_Account.json')

# Load credentials
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build('drive', 'v3', credentials=creds)

# Folder ID where you want to upload
FOLDER_ID = '1iajsRfYZ8c0H5bwzLB1SXiY8EkcutGjo'

file_metadata = {'name': 'test.pdf', 'parents': [FOLDER_ID]}
media = MediaFileUpload(pdf_file, mimetype='application/pdf')

file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
print("Uploaded file ID:", file.get('id'))