# gapitoo

A lightweight Python package to interact with Google Drive. This package simplifies uploading and downloading files by encapsulating Google Drive API operations within a simple class structure.

## Features

- **Easy Authentication:** Automatically handles authentication using OAuth 2.0 with token caching.
- **File Upload:** Upload files to any Google Drive folder using either folder ID or URL.
- **File Download:** Download files from Google Drive by providing a file ID or URL.

## Installation
1. **Clone the Repository:**

   ```bash
   git clone https://github.com/melonheader/gapitoo.git
   cd gapitoo
   ```

2. **Create a Virtual Environment (Optional):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -e .
   ```

## Configuration

Before using the package, ensure you have your Google API credentials:

1. **Credentials File:** Place your Google OAuth 2.0 client secrets JSON file in a folder (default path used in the package is `gcon/creds.json`).
2. **Token Caching:** The package stores authentication tokens in `token.pickle`. Make sure the folder has appropriate write permissions.

## Usage

```python
from gapitoo import gdservice

# Initialize the Google Drive service
drive = gdservice(creds_file='gcon/creds.json', token_file='token.pickle')

# Upload a file by providing the folder URL
folder_url = f"https://drive.google.com/drive/folders/{YOUR_FOLDER_ID}?usp=sharing"
uploaded_file_id = drive.upload("path/to/your/file.txt", drive_folder_url=folder_url)
## or folder ID
uploaded_file_id = drive.upload("path/to/your/file.txt", drive_folder_id=YOUR_FOLDER_ID)

# Download a file by providing the file URL
file_url = f"https://drive.google.com/file/d/{uploaded_file_id}/view?usp=sharing"
drive.download("path/to/destination/file.txt", drive_file_url=file_url)
## or file ID
drive.download("path/to/destination/file.txt", drive_file_id=uploaded_file_id)
```

## API Reference

### Class: `gdservice`

#### `__init__(creds_file: str, token_file: str)`
- Initializes the Google Drive service.
- **Parameters:**
  - `creds_file`: Path to the credentials JSON file.
  - `token_file`: Path to the token pickle file.

#### `upload(file_path: str, drive_folder_id: str = None, drive_folder_url: str = None)`
- Uploads a file to Google Drive.
- **Parameters:**
  - `file_path`: Local path to the file to be uploaded.
  - `drive_folder_id`: (Optional) Google Drive folder ID.
  - `drive_folder_url`: (Optional) URL of the destination folder.
- **Returns:** The uploaded file's ID.

#### `download(destination_path: str, drive_file_id: str = None, drive_file_urp: str = None)`
- Downloads a file from Google Drive.
- **Parameters:**
  - `destination_path`: Local path where the file will be saved.
  - `drive_file_id`: (Optional) Google Drive file ID.
  - `drive_file_urp`: (Optional) URL of the file to download.

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This package is provided "as is" without any warranty. Use it at your own risk.
