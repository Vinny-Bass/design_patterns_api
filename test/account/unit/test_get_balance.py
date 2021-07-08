import unittest
import os
from providers.customer.customer_provider import CustomerProvider
from domain.account.use_cases.get_balance import GetBalance


class TestGetBalance(unittest.TestCase):

    def test_get_balance(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../../clients_test.json')
        provider = CustomerProvider(filename, 1)
        balance = GetBalance(provider).execute('81656efe-609d-4fdd-99ca-27c1d123c215')
        self.assertEqual(balance, 200)
