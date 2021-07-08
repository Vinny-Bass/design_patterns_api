from providers.customer.base_contract import BaseContract


class ReceiveTransfer:

    def __init__(self, customer_provider: BaseContract):
        self.customer_provider = customer_provider

    def execute(self, amount, account_id, payer_account_id):
        return self.customer_provider.receive_transfer(amount, account_id, payer_account_id)
