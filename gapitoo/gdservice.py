import os
import pickle
import io
import re
from tqdm import tqdm
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']

class gdservice:
    def __init__(self, creds_file: str = 'gcon/creds.json', token_file: str = 'token.pickle'):
        """Initializes the Google Drive service.
        
        Args:
            creds_file (str): Path to the credentials JSON file.
            token_file (str): Path to the token pickle file.
        """
        self.creds = None
        self.token_file = token_file

        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                self.creds = pickle.load(token)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    creds_file, SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob'
                )
                auth_url, _ = flow.authorization_url(access_type='offline', prompt='consent')
                print("Authorize the request by visiting this URL:", auth_url)
                code = input("Enter the authorization code: ")
                flow.fetch_token(code=code)
                self.creds = flow.credentials

            with open(token_file, 'wb') as token:
                pickle.dump(self.creds, token)
        
        self.service = build('drive', 'v3', credentials=self.creds)

    def upload(self, file_path: str, drive_folder_id: str = None, drive_folder_url: str = None):
        """Uploads a file to Google Drive.
        
        Args:
            file_path (str): Local path to the file to be uploaded.
            drive_folder_id (str): ID of the destination folder on Google Drive.
            drive_folder_url (str): URL of the destination folder on Google Drive.
        """
        if not drive_folder_id:
            if not drive_folder_url:
                print("Provide either the drive_folder_id or the drive_folder_url")
                return
            lhs = 'https://drive.google.com/drive/folders/'
            rhs = '?usp='
            pattern = rf'{re.escape(lhs)}([^/]+){re.escape(rhs)}'
            sstring = re.search(pattern, drive_folder_url)
            if sstring:
                drive_folder_id = sstring.group(1)
            else:
                print("Double check the provided URL")
        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [drive_folder_id]
        }
        media = MediaFileUpload(file_path, resumable=True)
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f"{os.path.basename(file_path)} uploaded; File ID: {file.get('id')}")
        return file.get('id')

    def download(self, destination_path: str, drive_file_id: str = None, drive_file_url: str = None):
        """Downloads a file from Google Drive.
        
        Args:
            file_id (str): ID of the file to be downloaded.
            drive_file_id (str): ID of the target file on Google Drive.
            drive_file_url (str): URL of the target file on Google Drive.
        """
        if not drive_file_id:
            if not drive_file_url:
                print("Provide either the file ID or the file URL")
                return
            lhs = 'https://drive.google.com/file/d/'
            rhs = '/view?usp='
            pattern = rf'{re.escape(lhs)}([^/]+){re.escape(rhs)}'
            pattern = r'd/([^/]+)/view'
            sstring = re.search(pattern, drive_file_url)
            if sstring:
                drive_file_id = sstring.group(1)
            else:
                print("Double check the provided URL")

        request = self.service.files().get_media(fileId=drive_file_id)
        fh = io.FileIO(destination_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)

        # try to get the file size for progress display
        file_metadata = self.service.files().get(fileId=drive_file_id, fields="size").execute()
        file_size = int(file_metadata.get('size', 0))  # fallback to 0 if size is unavailable

        print(f"Downloading to {destination_path}...")
        with tqdm(total=file_size, unit='B', unit_scale=True, desc="Download Progress") as pbar:
            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    pbar.update(status.resumable_progress)
