from abc import ABC, abstractmethod


class BaseContract(ABC):

    def __init__(self, file_path, customer_id):
        self.file_path = file_path
        self.customer_id = customer_id

    @abstractmethod
    def get_customer(self):
        pass

    @abstractmethod
    def get_account(self, account_id):
        pass

    @abstractmethod
    def add_account(self, new_account):
        pass

    @abstractmethod
    def make_transfer(self, amount, destiny_account):
        pass
