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
CLIENT_SECRET_FILE = {
  "type": "service_account",
  "project_id": "taxes-492518",
  "private_key_id": "d4cd4b907b67aadb02b284f62b38821c14716d84",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC6GWhWlsUMy/bC\nG8/5R5hB8keKoZRwiTKsOGBl+5XLKE8s3dbuPmmElxFGq3rleQcOu23CD3yBc6wW\newwAPsI9i1DLzTLK/Khf5EVKo8eXpk8A6N8oLmv399UcGrgu4Vp8OWNmTGlBR8/K\nqzufJ/kGknDEFt+Hm6OH1v5Q4OLtpV8B4hXnqEirpuvD8rLdcemGif6E1NVkN6wA\nc284W3NeqI9jgDUX9585DluKrVnNsV3jWz+jp4mIDeJXY+HIkHGKwdK4f4dhYauH\ngTjznkBd+dicHo11uNsCSQkVGYbnu+iIYWAEJmQNIAdQgNLI6Cb6+R9QbL6fHbYD\na+AFX/05AgMBAAECggEAA1n4SVDrSQz2S24dS3e42/0tQSeiSPmLjlLwl32Vp8Q4\n0s3G9GDu3QqsbrmhW7cXg7In6p4FR76Jy5jZMTrwHBQhdx4hq0qsDJgLkGnNKyO9\nWf6XoD1fx+YwchJgHUYFL2YILnwzTA/rQ9LcHsRlRXNHMRzZVzOcGRLr3xCBvbZc\nE7JyysRR8Fhc/ZbBv9piIcLe4B0C8tbyHjoL8UpNipOfzi76rjVwSttudd/2fmwm\nHQIuyYKM9gwef9ax4NodcYnIa+im8GgnH/PB6I2KLV15YPGY0Lh765xJI4LksLZm\nBvg7obcJbfTAoBeUQOkhuvZbMCM9lZ32azjHqKtY4QKBgQDpj5fxBV9P9vXKqyM1\nIsKq1ktEWUjt+Kv7x7J8zfW4jg3Nl8mdIwIV1CUHWG1mePwX3JgoSzegeua7Wbk/\nWCILrMglXPYjTGzPbpzBjmXm3Nj+NzmYggLe31pEnHsc9n57CWHWbtp54egWOoD4\nOYruEPdC7YiMyhlgtT2GDuMc8QKBgQDL+n/UeX8ZNJlp/J0YoOYEJcB1vZnhfM/3\nwygMNU+yRfer4EHf+3C8ylHAzGBMLXjN0/FIG1wfzFXwZQhzy3pRViURCYgDmfPS\nlb7rC8JACfYf4Avjlcf1EQw2VcyEKihj7TyuoXX2bOaV243L0BSVWUKFB6UU9ev6\nYgnwBEKEyQKBgBtowZEEa2IL/l5RZSlYMfYwfdbAj6F1vGEo11Z0KTEGYrJM7Nkn\nAZikM9A/3V7YNeVq+uRHp3iK08cKyYWYhy5NkZNo7G3KCz7woS7J0kWch06WFolC\nQKn9Fi/VGVGVz9QKjtPGYJdLHpx1MytuPVKg5ROSoqK7GO1Td6vi1V5RAoGALFLt\nrh0MmkyMvbQv6ucjtGkDrlIZ+x6lDmCw9h4riECd9hJQHjzEHbIVG8ENd+A1rPxO\nJO4VEa/USN2bfZYMqVn/yfj5PlcY3Xy+tNKkTkgb3IdR7g1hGwauUaxJObrzdeta\nUVQyju7RGGVSJaS8pEt2IfQsUiayNYFSSX6TeckCgYAyTFJqbuBDwvlCVrC+jDdW\nU3Cg/4MvgeDMlodu+tr/i+6kAD0uU2RZnHvm3AEw14QlY2sQgnlTymRLhx0UXVSE\nXN9EDu+2c10/n15nECuopGzDGFKr3ESY+Xzuej+GASYirJZRHSfvvPOUXk099sDy\nzivam9T0/39G5k9Cf5Q1uQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "t-287-418@taxes-492518.iam.gserviceaccount.com",
  "client_id": "101707497507102061244",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/t-287-418%40taxes-492518.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


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
    
    folder_id = "1X7OA9TyD7cVTYXhLrj--Z_T7mQqXu5nt"  # your folder ID
    file_id = upload_to_drive(pdf_file, folder_id)
    st.success(f"Uploaded to Google Drive!\nFile ID: {file_id}\nFolder ID: {folder_id}")
