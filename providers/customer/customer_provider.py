import json
import datetime
from providers.customer.base_contract import BaseContract


class CustomerProvider(BaseContract):

    def get_customer(self):
        with open(self.file_path) as file:
            clients = json.load(file)

        return next((customer for customer in clients if customer['id'] == self.customer_id), {})

    def get_account(self, account_id):
        customer = self.get_customer()

        if customer == {}:
            raise Exception(f'Customer with id {self.customer_id} don\'t exists')

        account = next((account for account in customer['accounts'] if account['id'] == account_id), {})

        if account == {}:
            raise Exception(f'Customer don\'t have the account {account_id} ')

        return account

    def add_account(self, new_account):
        with open(self.file_path) as file:
            clients = json.load(file)

        customer = self.get_customer()

        if customer == {}:
            raise Exception(f'Customer with id {self.customer_id} don\'t exists')

        customer['accounts'].append(new_account)

        for index, c in enumerate(clients):
            if c['id'] == self.customer_id:
                clients[index] = customer

        with open(self.file_path, 'w') as file:
            json.dump(clients, file)

        return new_account

    def make_transfer(self, amount, account_id, destiny_account_id):
        with open(self.file_path) as file:
            clients = json.load(file)

        customer = self.get_customer()

        if customer == {}:
            raise Exception(f'Customer with id {self.customer_id} don\'t exists')

        account = self.get_account(account_id)

        account['balance'] -= amount
        new_transfer = {
            'to': destiny_account_id,
            'amount': amount,
            'when': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        }
        account['transfers'].append(new_transfer)

        for index, c in enumerate(clients):
            if c['id'] == self.customer_id:
                for i, a in enumerate(c['accounts']):
                    if a['id'] == account['id']:
                        clients[index]['accounts'][i] = account

        with open(self.file_path, 'w') as file:
            json.dump(clients, file)

        return new_transfer

    def receive_transfer(self, amount, account_id, payer_account_id):
        with open(self.file_path) as file:
            clients = json.load(file)

        customer = self.get_customer()

        if customer == {}:
            raise Exception(f'Customer with id {self.customer_id} don\'t exists')

        account = self.get_account(account_id)

        account['balance'] += amount
        new_transfer = {
            'from': payer_account_id,
            'amount': amount,
            'when': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        }
        account['transfers'].append(new_transfer)

        for index, c in enumerate(clients):
            if c['id'] == self.customer_id:
                for i, a in enumerate(c['accounts']):
                    if a['id'] == account['id']:
                        clients[index]['accounts'][i] = account

        with open(self.file_path, 'w') as file:
            json.dump(clients, file)

        return new_transfer
