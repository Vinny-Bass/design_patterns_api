import os
from flask import Flask, jsonify, request
from domain.account.use_cases.get_balance import GetBalance
from domain.account.use_cases.get_transfers import GetTransfers
from domain.account.use_cases.create_account import CreateAccount
from domain.account.use_cases.make_transfer import MakeTransfer
from domain.account.use_cases.receive_transfer import ReceiveTransfer
from providers.customer.customer_provider import CustomerProvider
from middlewares import create_account_middleware, make_transfer_middleware


app = Flask(__name__)

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, './clients.json')


@app.route("/account/create/<int:client_id>", methods=["POST"])
@create_account_middleware
def create_account(client_id):
    try:
        if request.json and request.json.get('initial_amount'):
            initial_amount = int(request.json.get('initial_amount'))
        else:
            initial_amount = 0

        customer_provider = CustomerProvider(filename, client_id)
        created_account = CreateAccount(customer_provider).execute(initial_amount)

        return jsonify({
            'client_id': client_id,
            'account_id': created_account['id'],
            'balance': created_account['balance']
        })
    except Exception as error:
        return jsonify({'error': str(error)}), 400


@app.route("/account/balance/<int:client_id>/<string:account_id>")
def get_balance(client_id, account_id):
    try:
        customer_provider = CustomerProvider(filename, client_id)

        balance = GetBalance(customer_provider).execute(account_id)

        return jsonify({
            'client_id': client_id,
            'account_id': account_id,
            'balance': balance
        })
    except Exception as error:
        return jsonify({'error': str(error)}), 400


@app.route("/account/transfers/<int:client_id>/<string:account_id>")
def get_transfers(client_id, account_id):
    try:
        customer_provider = CustomerProvider(filename, client_id)

        transfers = GetTransfers(customer_provider).execute(account_id)

        return jsonify({
            'client_id': client_id,
            'account_id': account_id,
            'transfers': transfers
        })
    except Exception as error:
        return jsonify({'error': str(error)}), 400


@app.route("/account/transfer", methods=["POST"])
@make_transfer_middleware
def transfer():
    try:
        payer = request.json.get('payer')
        receiver = request.json.get('receiver')

        payer_provider = CustomerProvider(filename, payer['client_id'])
        receiver_provider = CustomerProvider(filename, receiver['client_id'])

        payer_transfer = MakeTransfer(payer_provider)
        payer_transfer.execute(payer['amount'], payer['account_id'], receiver['account_id'])

        receiver_transfer = ReceiveTransfer(receiver_provider)
        receiver_transfer.execute(payer['amount'], receiver['account_id'], payer['account_id'])

        return jsonify({'message': 'The transfer was successful.'})
    except Exception as error:
        return jsonify({'error': str(error)}), 400


if __name__ == "__main__":
    app.run(debug=True)
