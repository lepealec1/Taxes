from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

# --- Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'Service_Account.json')
SCOPES = ['https://www.googleapis.com/auth/drive']

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('drive', 'v3', credentials=creds)

# --- Create Folder ---
folder_metadata = {
    'name': 'ServiceAccountFolder',
    'mimeType': 'application/vnd.google-apps.folder'
}
folder = service.files().create(body=folder_metadata, fields='id').execute()
folder_id = folder.get('id')
print("Folder created with ID:", folder_id)

# --- Share Folder with Your Email ---
user_email = "lepealec518@gmail.com"  # <-- replace with your Gmail
permission = {
    'type': 'user',
    'role': 'writer',  # can also use 'reader'
    'emailAddress': user_email
}

service.permissions().create(
    fileId=folder_id,
    body=permission,
    fields='id',
).execute()

print(f"Folder shared with {user_email}. View at: https://drive.google.com/drive/folders/{folder_id}")