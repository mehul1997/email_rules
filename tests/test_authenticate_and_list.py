import unittest
from unittest.mock import patch, MagicMock

from idna.idnadata import scripts
from googleapiclient.discovery import build

from email_rules.scripts.authenticate_and_list import (
    authenticate,
    list_emails,
    get_email_details,
    mark_as_read,
    mark_as_unread,
    archive_email
)

class TestGmailFunctions(unittest.TestCase):
    #
    # @patch('email_rules.scripts.authenticate_and_list.os.path.exists')
    # @patch('email_rules.scripts.authenticate_and_list.pickle.load')
    # def test_authenticate_existing_token(self, mock_pickle_load, mock_path_exists):
    #     mock_path_exists.return_value = True
    #     mock_creds = MagicMock()
    #     mock_creds.valid = True
    #     mock_pickle_load.return_value = mock_creds
    #
    #     creds = authenticate()
    #     self.assertEqual(creds, mock_creds)


    def test_authenticate_real(self):
        creds = authenticate()
        service = build('gmail', 'v1', credentials=creds)
        self.assertIsNotNone(service)

    def test_list_emails_real(self):
        creds = authenticate()
        service = build('gmail', 'v1', credentials=creds)
        ids = list_emails(service)
        self.assertIsInstance(ids, list)

    def test_get_email_details_all_headers(self):
        service = MagicMock()
        msg_id = '12345'
        service.users.return_value.messages.return_value.get.return_value.execute.return_value = {
            'payload': {
                'headers': [
                    {'name': 'From', 'value': 'sender@example.com'},
                    {'name': 'Subject', 'value': 'Test Subject'},
                    {'name': 'Date', 'value': 'Thu, 11 Sep 2025 09:19:30 GMT'}
                ]
            }
        }

        result = get_email_details(service, msg_id)

        expected = {
            'id': msg_id,
            'from': 'sender@example.com',
            'subject': 'Test Subject',
            'date': 'Thu, 11 Sep 2025 09:19:30 GMT'
        }

        self.assertEqual(result, expected)

    def test_mark_as_read_calls_api_correctly(self):
        service = MagicMock()
        msg_id = 'abc123'

        mark_as_read(service, msg_id)

        # Assert that the modify() method was called with correct arguments
        service.users.return_value.messages.return_value.modify.assert_called_once_with(
            userId='me',
            id=msg_id,
            body={'removeLabelIds': ['UNREAD']}
        )

        # Assert that execute() was called after modify()
        service.users.return_value.messages.return_value.modify.return_value.execute.assert_called_once()

    def test_mark_as_unread_calls_api_correctly(self):
        service = MagicMock()
        msg_id = 'abc123'

        mark_as_unread(service, msg_id)

        # Assert that the modify() method was called with correct arguments
        service.users.return_value.messages.return_value.modify.assert_called_once_with(
            userId='me',
            id=msg_id,
            body={'addLabelIds': ['UNREAD']}
        )

        # Assert that execute() was called after modify()
        service.users.return_value.messages.return_value.modify.return_value.execute.assert_called_once()

    def test_archive_email_calls_api_correctly(self):
        service = MagicMock()
        msg_id = 'abc123'

        archive_email(service, msg_id)

        # Assert that the modify() method was called with correct arguments
        service.users.return_value.messages.return_value.modify.assert_called_once_with(
            userId='me',
            id=msg_id,
            body={'removeLabelIds': ['INBOX']}
        )

        # Assert that execute() was called after modify()
        service.users.return_value.messages.return_value.modify.return_value.execute.assert_called_once()

if __name__ == '__main__':
    unittest.main()
