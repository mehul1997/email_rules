import unittest
from unittest.mock import mock_open, patch
from email_rules.scripts.rules import load_rules, apply_rules


class TestLoadRules(unittest.TestCase):
    def test_load_rules(self):
        mock_data = '''
        {
            "predicate": "All",
            "rules": [
                {
                    "field": "from",
                    "predicate": "contains",
                    "value": "example@example.com"
                }
            ],
            "actions": ["mark_as_read"]
        }
        '''

        with patch('builtins.open', mock_open(read_data=mock_data)):
            rules = load_rules()

        self.assertEqual(rules['predicate'], 'All')
        self.assertEqual(len(rules['rules']), 1)
        self.assertEqual(rules['rules'][0]['field'], 'from')

    def test_contains_predicate_matches(self):
        email = {
            'from': 'info@example.com',
            'subject': 'Welcome to the platform',
            'date': 'Thu, 11 Sep 2025 09:19:30 GMT'
        }
        rules = {
            'predicate': 'All',
            'rules': [
                {
                    'field': 'from',
                    'predicate': 'contains',
                    'value': 'info'
                }
            ]
        }
        result = apply_rules(email, rules)
        self.assertTrue(result)

    def test_date_less_than(self):
        email = {
            'from': 'info@example.com',
            'subject': 'Reminder',
            'date': 'Thu, 11 Sep 2023 09:19:30 GMT'
        }
        rules = {
            'predicate': 'All',
            'rules': [
                {
                    'field': 'date',
                    'predicate': 'less_than',
                    'value': '2024-01-01'
                }
            ]
        }
        result = apply_rules(email, rules)
        self.assertTrue(result)

    def test_date_greater_than(self):
        email = {
            'from': 'info@example.com',
            'subject': 'Reminder',
            'date': 'Thu, 11 Sep 2025 09:19:30 GMT'
        }
        rules = {
            'predicate': 'All',
            'rules': [
                {
                    'field': 'date',
                    'predicate': 'greater_than',
                    'value': '2024-01-01'
                }
            ]
        }
        result = apply_rules(email, rules)
        self.assertTrue(result)

    def test_all_predicate(self):
        email = {
            'from': 'info@example.com',
            'subject': 'Welcome',
            'date': 'Thu, 11 Sep 2025 09:19:30 GMT'
        }
        rules = {
            'predicate': 'All',
            'rules': [
                {
                    'field': 'from',
                    'predicate': 'contains',
                    'value': 'info'
                },
                {
                    'field': 'subject',
                    'predicate': 'contains',
                    'value': 'Welcome'
                }
            ]
        }
        result = apply_rules(email, rules)
        self.assertTrue(result)

    def test_any_predicate(self):
        email = {
            'from': 'unknown@example.com',
            'subject': 'Hello',
            'date': 'Thu, 11 Sep 2025 09:19:30 GMT'
        }
        rules = {
            'predicate': 'Any',
            'rules': [
                {
                    'field': 'from',
                    'predicate': 'contains',
                    'value': 'info'
                },
                {
                    'field': 'subject',
                    'predicate': 'contains',
                    'value': 'Hello'
                }
            ]
        }
        result = apply_rules(email, rules)
        self.assertTrue(result)