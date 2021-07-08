from providers.customer.base_contract import BaseContract


class MakeTransfer:

    def __init__(self, customer_provider: BaseContract):
        self.customer_provider = customer_provider

    def execute(self, amount, account_id, destiny_account_id):
        account = self.customer_provider.get_account(account_id)

        if account['balance'] < amount:
            raise Exception('Insuficient founds')

        return self.customer_provider.make_transfer(amount, account_id, destiny_account_id)
