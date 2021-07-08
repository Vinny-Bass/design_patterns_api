from providers.customer.base_contract import BaseContract


class GetBalance:

    def __init__(self, customer_provider: BaseContract):
        self.customer_provider = customer_provider

    def execute(self, account_id):
        account = self.customer_provider.get_account(account_id)
        return account['balance']
