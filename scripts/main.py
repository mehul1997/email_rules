import sys
import os

# Get the absolute path of the parent directory (email_rules/)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Append it to sys.path
sys.path.append(parent_dir)

from config.database import connect_db, create_table, save_email, fetch_all_emails, table_exists, fetch_email
from authenticate_and_list import authenticate, get_email_details, list_emails, mark_as_read, mark_as_unread, archive_email
from googleapiclient.discovery import build
from rules import load_rules, apply_rules

def main():
    conn = connect_db()
    if table_exists(conn, 'emails'):
        print("Table already exists.")
    else:
        print("Table does not exist. Creating now...")
        create_table(conn)

    # Example: saving emails after fetching
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)
    ids = list_emails(service)
    for msg in ids:
        email = get_email_details(service, msg['id'])
        record = fetch_email(conn, "emails", msg['id'])
        if not record:
            save_email(conn, email)
        else:
            print("Record already exists")

    rules = load_rules()
    emails = fetch_all_emails(conn)
    for email in emails:
        print("Checking Email: {}".format(email))
        email_dict = {
            'id': email[0],
            'from': email[1],
            'subject': email[2],
            'date': email[3]
        }
        if apply_rules(email_dict, rules):
            print(f"Email {email[0]} matches rules!")
            for action in rules.get('actions', []):
                if action == "mark_as_read":
                    mark_as_read(service, email[0])
                elif action == "mark_as_unread":
                    mark_as_unread(service, email[0])
                elif action == "archive":
                    archive_email(service, email[0])
                    pass
        else:
            print(f"Email {email[0]} does not match rules.")

    conn.close()


if __name__ == '__main__':
    main()