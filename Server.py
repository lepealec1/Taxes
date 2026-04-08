import streamlit as st
import pickle
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

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