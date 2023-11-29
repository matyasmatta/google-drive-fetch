import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
import io
from googleapiclient.errors import HttpError

# Replace 'path/to/your/credentials.json' with the path to your service account JSON key file
credentials = service_account.Credentials.from_service_account_file('D:/Dokumenty/Klíče/credentials.json', scopes=['https://www.googleapis.com/auth/drive'])

# Build the Drive API service
drive_service = build('drive', 'v3', credentials=credentials)

def list_files():
    response = drive_service.files().list(pageSize=1000, fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)", q='name contains "e"').execute()

    files = response.get('files', [])

    if not files:
        print('No files found.')
    else:
        print('Files:')
        for file in files:
            print(f"{file['name']} ({file['id']})")
            download_file(file['id'], file['name'])

def download_file(file_id, file_name):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_name, 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%")

if __name__ == '__main__':
    list_files()
