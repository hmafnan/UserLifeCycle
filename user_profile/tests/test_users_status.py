import django

django.setup()
import os
import sys

# To run from cmd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from user_profile.tests.utility import build_url
import unittest
from django.test import Client


class TestActiveDaysByUser(unittest.TestCase):
    """Test active days for given user"""

    def setUp(self):
        self.client = Client()
        self.user_id = 'user_000000BcyxC7NwL6OnB9boEXLUNBw'

    def test_days_active_for_user(self):
        actual_days_active = 153
        response = self.client.get(
            build_url('days_active', params={'user_id': self.user_id}),
            content_type='application/json')
        self.assertEqual(actual_days_active,
                         response.json()['days_active'], 'Expected days active not matches')

    def test_days_active_for_user_with_optional_params(self):
        month = 5
        underwriter = 'blue'
        actual_days_active = 31
        response = self.client.get(
            build_url('days_active', params={'user_id': self.user_id, 'month': month, 'underwriter': underwriter}),
            content_type='application/json')
        self.assertEqual(actual_days_active,
                         response.json()['days_active'], 'Expected days active not matches')


class TestNewUsersByDate(unittest.TestCase):
    """Test new users count for given date"""

    def setUp(self):
        self.client = Client()
        self.date = '2020-03-29'

    def test_new_users_for_date(self):
        actual_users = 7
        response = self.client.get(
            build_url('new_users', params={'date': self.date}),
            content_type='application/json')
        self.assertEqual(actual_users,
                         response.json()['new_users_count'],
                         'Expected new users count not matches')

    def test_new_users_for_date_with_optional_params(self):
        month = 5
        underwriter = 'blue'
        actual_days_active = 4
        response = self.client.get(
            build_url('new_users', params={'date': self.date, 'month': month, 'underwriter': underwriter}),
            content_type='application/json')
        self.assertEqual(actual_days_active,
                         response.json()['new_users_count'],
                         'Expected new users count not matches with optional params')


class TestLapsedUsersByMonth(unittest.TestCase):
    """Test lapsed users count for given month"""

    def setUp(self):
        self.client = Client()
        self.month = '3'

    def test_lapsed_users_for_month(self):
        actual_users = 3
        response = self.client.get(
            build_url('lapsed_users', params={'month': self.month}),
            content_type='application/json')
        self.assertEqual(actual_users,
                         response.json()['lapsed_users_count'],
                         'Expected lapsed users count not matches')


class TestNewUsersPremiumByUnderwriter(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.underwriter = 'blue'

    def test_new_users_premium_for_underwriter(self):
        actual_results = [{'date': '2020-03', 'premium': 197}, {'date': '2020-04', 'premium': 38}]
        response = self.client.get(
            build_url('new_users_premium', params={'underwriter': self.underwriter}),
            content_type='application/json')
        self.assertListEqual(actual_results,
                             response.json(),
                             'Expected new users premium count not matches')

    def test_new_users_premium_for_underwriter_with_optional_params(self):
        month = 4
        actual_results = [{'date': '2020-04', 'premium': 38}]
        response = self.client.get(
            build_url('new_users_premium', params={'underwriter': self.underwriter, 'month': month}),
            content_type='application/json')
        self.assertListEqual(actual_results,
                             response.json(),
                             'Expected new users premium count not matches with optional params')


if __name__ == '__main__':
    unittest.main()
