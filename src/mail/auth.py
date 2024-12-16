import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define scopes and credentials file path
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
CREDENTIALS_PATH = "credentials.json"
TOKEN_PATH = "token.json"

def authenticate_and_save_credentials():
    """
    Authenticate the user and save the credentials to a file.
    """
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
    creds = flow.run_local_server(port=0)

    # Save credentials for future use
    with open(TOKEN_PATH, "w", encoding="utf-8") as token_file:
        token_file.write(creds.to_json())
    print("Authentication successful. Credentials saved.")

def load_credentials():
    """
    Load saved credentials from the token file or prompt the user to authenticate.
    Returns:
        Credentials object for Gmail API access.
    """
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "r", encoding="utf-8") as token_file:
            creds_data = json.load(token_file)
        return Credentials.from_authorized_user_info(creds_data, SCOPES)
    else:
        print("No credentials found. Please authenticate first.")
        authenticate_and_save_credentials()
        return load_credentials()

def get_gmail_service():
    """
    Get an authorized Gmail API service instance.
    Returns:
        Authorized Gmail API service.
    """
    creds = load_credentials()
    return build("gmail", "v1", credentials=creds)
