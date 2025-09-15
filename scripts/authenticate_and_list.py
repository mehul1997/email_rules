import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import yaml

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load constants.yml
constants_path = os.path.join(BASE_DIR, '..', 'config', 'constants.yml')
with open(constants_path, 'r') as file:
    constants = yaml.safe_load(file)

NUMBER_OF_EMAIL_LIMIT = constants['NUMBER_OF_EMAIL_LIMIT']

def authenticate():
    creds = None

    token_path = os.path.join(BASE_DIR, '..', 'data', 'token.json')
    cred_path = os.path.join(BASE_DIR, '..', 'credentials', 'credentials.json')

    # Load existing token if available
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token_file:
            creds = pickle.load(token_file)

    # If no valid credentials, go through OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for next time
        with open(token_path, 'wb') as token_file:
            pickle.dump(creds, token_file)
    return creds

def list_emails(service):
    # Fetch the first 5 emails from the inbox
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=NUMBER_OF_EMAIL_LIMIT).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No emails found.")
    else:
        print("Emails:")
        for msg in messages:
            print(f" - ID: {msg['id']}")
        return messages

def get_email_details(service, msg_id):
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    headers = msg['payload']['headers']

    email_data = {'id': msg_id}
    for header in headers:
        if header['name'] == 'From':
            email_data['from'] = header['value']
        if header['name'] == 'Subject':
            email_data['subject'] = header['value']
        if header['name'] == 'Date':
            email_data['date'] = header['value']
    return email_data

def mark_as_read(service, msg_id):
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()
    print(f"Message {msg_id} marked as read.")

def mark_as_unread(service, msg_id):
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'addLabelIds': ['UNREAD']}
    ).execute()
    print(f"Message {msg_id} marked as unread.")

def archive_email(service, msg_id):
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'removeLabelIds': ['INBOX']}
    ).execute()
    print(f"Message {msg_id} archived.")
