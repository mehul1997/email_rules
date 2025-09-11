import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate():
    print("Enter authenticate")
    creds = None
    token_path = '../data/token.json'
    print(token_path)
    cred_path = '../credentials/credentials.json'
    print(cred_path)

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
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=5).execute()
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

def main():
    print("hello")
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)
    ids = list_emails(service)
    email_data = get_email_details(service, ids[0]['id'])
    print(email_data)

if __name__ == "__main__":
    main()
