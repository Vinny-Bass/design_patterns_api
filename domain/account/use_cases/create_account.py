import uuid
from providers.customer.base_contract import BaseContract


class CreateAccount:

    def __init__(self, customer_provider: BaseContract):
        self.customer_provider = customer_provider

    def execute(self, initial_amount):
        new_account = {
            'id': str(uuid.uuid4()),
            'balance': initial_amount,
            'transfers': []
        }
        return self.customer_provider.add_account(new_account)
