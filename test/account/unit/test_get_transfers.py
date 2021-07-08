import unittest
import os
from providers.customer.customer_provider import CustomerProvider
from domain.account.use_cases.get_transfers import GetTransfers


class TestGetTransfers(unittest.TestCase):

    def test_get_transfers(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../../clients_test.json')
        provider = CustomerProvider(filename, 1)
        transfers = GetTransfers(provider).execute('81656efe-609d-4fdd-99ca-27c1d123c215')
        self.assertEqual(len(transfers), 0)
