import os
import pickle
import streamlit as st
from fpdf import FPDF
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

TOKEN_FILE = "token.pkl"
SCOPES = ['https://www.googleapis.com/auth/drive.file']
FOLDER_ID = "1X7OA9TyD7cVTYXhLrj--Z_T7mQqXu5nt"  # Your folder ID

# ----------------------------
# Get Drive service using OAuth
# ----------------------------
def get_drive_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_config(
            {
                "web": {
                    "client_id": st.secrets["google_oauth"]["client_id"],
                    "client_secret": st.secrets["google_oauth"]["client_secret"],
                    "auth_uri": st.secrets["google_oauth"]["auth_uri"],
                    "token_uri": st.secrets["google_oauth"]["token_uri"],
                    "redirect_uris": st.secrets["google_oauth"]["redirect_uris"]
                }
            },
            scopes=SCOPES
        )

        # This will run a Streamlit-friendly local server for OAuth
        creds = flow.run_local_server(port=0)

        # Save token for reuse
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return build('drive', 'v3', credentials=creds)

# ----------------------------
# Upload PDF
# ----------------------------
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

# ----------------------------
# PDF Generation Example
# ----------------------------
def generate_pdf(filename="example.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Sample PDF Upload", ln=True)
    pdf.output(filename)
    return filename

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("Upload PDF to Google Drive")

if st.button("Generate & Upload PDF"):
    pdf_file = generate_pdf()
    st.success(f"PDF generated: {pdf_file}")
    try:
        file_id = upload_to_drive(pdf_file)
        st.success(f"Uploaded! File ID: {file_id}")
        st.balloons()
    except Exception as e:
        st.error(f"Upload failed: {e}")