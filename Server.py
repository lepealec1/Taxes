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