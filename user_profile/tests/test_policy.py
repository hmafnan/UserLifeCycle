import django

django.setup()
import os
import sys

# To run from cmd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from user_profile.tests.utility import build_url
import unittest
from django.test import Client
from user_profile import models


class TestAllPolicy(unittest.TestCase):
    """Test expected behaviour for policies end points"""

    def setUp(self):
        self.client = Client()

    def test_all_policies(self):
        """Test all policies are returned"""
        response = self.client.get(build_url('policies'), content_type='application/json')
        actual_count = models.Policy.objects.count()
        self.assertEqual(actual_count, len(response.json()), 'Expected length not matches')

    def test_all_policies_with_optional_params(self):
        """Test filtered policies are returned with optional params
        """
        test_month = 3
        test_underwriter = 'blue'

        response = self.client.get(
            build_url('policies',
                      params={'month': test_month, 'underwriter': test_underwriter}),
            content_type='application/json')
        actual_count = models.Policy.objects.filter(
            policy_start_date__month=test_month,
            underwriter=test_underwriter).count()

        self.assertEqual(actual_count, len(response.json()), 'Expected length not matches')

    def test_all_policies_count_by_user(self):
        """Test actual policies count is returned for the the given user
        """
        user_id = 'user_000000BcyxC7NwL6OnB9boEXLUNBw'
        response = self.client.get(
            build_url('policy_count', params={'user_id': user_id}),
            content_type='application/json')
        actual_count = models.Policy.objects.filter(user_id=user_id).count()
        self.assertEqual(actual_count,
                         response.json()['policy_count'],
                         'Expected policies count not matches')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
