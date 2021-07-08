import unittest
import os
from providers.customer.customer_provider import CustomerProvider
from domain.account.use_cases.make_transfer import MakeTransfer
from domain.account.use_cases.get_balance import GetBalance
from domain.account.use_cases.get_transfers import GetTransfers


class TestGetTransfers(unittest.TestCase):

    def test_make_transfer(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../../clients_test.json')
        provider = CustomerProvider(filename, 1)
        transfer = MakeTransfer(provider).execute(20, '81656efe-609d-4fdd-99ca-27c1d123c215',
                                                  '869be46c-e74d-4d09-8b50-abfda8b783fa')
        self.assertEqual(len(list(transfer.keys())), 3)

        balance = GetBalance(provider).execute('81656efe-609d-4fdd-99ca-27c1d123c215')
        self.assertEqual(balance, 180)

        transfers = GetTransfers(provider).execute('81656efe-609d-4fdd-99ca-27c1d123c215')
        self.assertEqual(len(transfers), 1)

    def test_make_transfer_with_no_founds(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../../clients_test.json')
        provider = CustomerProvider(filename, 1)

        with self.assertRaises(Exception) as context:
            transfer = MakeTransfer(provider).execute(2000, '81656efe-609d-4fdd-99ca-27c1d123c215',
                                                      '869be46c-e74d-4d09-8b50-abfda8b783fa')
            self.assertTrue('Insuficient founds' in str(context.exception))
            balance = GetBalance(provider).execute('81656efe-609d-4fdd-99ca-27c1d123c215')
            self.assertEqual(balance, 200)

            transfers = GetTransfers(provider).execute('81656efe-609d-4fdd-99ca-27c1d123c215')
            self.assertEqual(len(transfers), 0)
