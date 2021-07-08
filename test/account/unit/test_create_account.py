import unittest
import os
from providers.customer.customer_provider import CustomerProvider
from domain.account.use_cases.create_account import CreateAccount


class TestCreateAccount(unittest.TestCase):

    def test_create_account(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../../clients_test.json')
        provider = CustomerProvider(filename, 1)
        new_account = CreateAccount(provider).execute(500)
        self.assertIn('id', new_account)
        self.assertIn('balance', new_account)
        self.assertEqual(new_account['balance'], 500)
        self.assertIn('transfers', new_account)
        self.assertEqual(new_account['transfers'], [])
