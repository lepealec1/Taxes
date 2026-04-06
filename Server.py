from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 1. OAuth scope for Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# 2. Run OAuth flow
flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json', SCOPES)
creds = flow.run_local_server(port=0)  # opens browser to login

# 3. Build Drive service
drive_service = build('drive', 'v3', credentials=creds)

# 4. Prepare file upload
file_metadata = {'name': 'questionnaire.pdf'}
media = MediaFileUpload('questionnaire.pdf', mimetype='application/pdf')

# 5. Upload to your personal Drive
file = drive_service.files().create(
    body=file_metadata,
    media_body=media,
    fields='id'
).execute()

print('Uploaded file ID:', file['id'])