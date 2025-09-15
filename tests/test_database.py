import unittest
import sqlite3
import os
import tempfile
from email_rules.config import database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory and database file
        self.test_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.test_dir.name, 'test_emails.db')
        self.conn = sqlite3.connect(self.db_path)

    def tearDown(self):
        # Close connection and cleanup
        self.conn.close()
        self.test_dir.cleanup()

    def test_create_table(self):
        database.create_table(self.conn)
        # Check if table exists
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='emails'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'emails')

    def test_save_and_fetch_email(self):
        database.create_table(self.conn)
        email = {
            'id': 'test1',
            'from': 'sender@example.com',
            'subject': 'Test Subject',
            'date': '2025-09-11'
        }
        database.save_email(self.conn, email)

        # Fetch email by ID
        fetched = database.fetch_email(self.conn, 'emails', 'test1')
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched[0], 'test1')
        self.assertEqual(fetched[1], 'sender@example.com')
        self.assertEqual(fetched[2], 'Test Subject')
        self.assertEqual(fetched[3], '2025-09-11')

    def test_fetch_all_emails(self):
        database.create_table(self.conn)
        emails = [
            {
                'id': 'test1',
                'from': 'sender1@example.com',
                'subject': 'First Email',
                'date': '2025-09-11'
            },
            {
                'id': 'test2',
                'from': 'sender2@example.com',
                'subject': 'Second Email',
                'date': '2025-09-12'
            }
        ]
        for email in emails:
            database.save_email(self.conn, email)

        fetched_emails = database.fetch_all_emails(self.conn)
        self.assertEqual(len(fetched_emails), 2)

    def test_table_exists(self):
        database.create_table(self.conn)
        exists = database.table_exists(self.conn, 'emails')
        self.assertTrue(exists)

        not_exists = database.table_exists(self.conn, 'non_existing')
        self.assertFalse(not_exists)

    def test_save_email_integrity_error(self):
        # Test that saving duplicate primary key replaces it due to INSERT OR REPLACE
        database.create_table(self.conn)
        email = {
            'id': 'test1',
            'from': 'sender@example.com',
            'subject': 'Test Subject',
            'date': '2025-09-11'
        }
        database.save_email(self.conn, email)
        # Save again with a different subject
        email['subject'] = 'Updated Subject'
        database.save_email(self.conn, email)

        fetched = database.fetch_email(self.conn, 'emails', 'test1')
        self.assertEqual(fetched[2], 'Updated Subject')

if __name__ == "__main__":
    unittest.main()
