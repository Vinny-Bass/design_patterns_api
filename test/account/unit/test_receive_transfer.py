import unittest
import os
from providers.customer.customer_provider import CustomerProvider
from domain.account.use_cases.receive_transfer import ReceiveTransfer
from domain.account.use_cases.get_balance import GetBalance
from domain.account.use_cases.get_transfers import GetTransfers


class TestReceiveTransfer(unittest.TestCase):

    def test_receive_transfer(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../../clients_test.json')
        provider = CustomerProvider(filename, 2)
        transfer = ReceiveTransfer(provider).execute(20, '869be46c-e74d-4d09-8b50-abfda8b783fa',
                                                     '81656efe-609d-4fdd-99ca-27c1d123c215')
        self.assertEqual(len(list(transfer.keys())), 3)

        balance = GetBalance(provider).execute('869be46c-e74d-4d09-8b50-abfda8b783fa')
        self.assertEqual(balance, 40)

        transfers = GetTransfers(provider).execute('869be46c-e74d-4d09-8b50-abfda8b783fa')
        self.assertEqual(len(transfers), 1)

