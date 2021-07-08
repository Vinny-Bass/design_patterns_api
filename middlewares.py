from functools import wraps
from flask import request, Response


def create_account_middleware(func):
    @wraps(func)
    def validate_params(*args, **kwargs):
        if request.json and request.json.get('initial_amount'):
            initial_amount = request.json.get('initial_amount')
            if not isinstance(initial_amount, int):
                return Response('The initial_amount param must be an integer', mimetype='text/plain', status=400)

        return func(*args, **kwargs)
    return validate_params


def make_transfer_middleware(func):
    @wraps(func)
    def validate_params(*args, **kwargs):
        if not request.json:
            return Response('Please send payer and receiver data', mimetype='text/plain', status=400)

        payer = request.json.get('payer')
        receiver = request.json.get('receiver')

        if not payer or not receiver:
            return Response('Please send payer and receiver data', mimetype='text/plain', status=400)

        rules = [
            'client_id' in payer,
            'client_id' in receiver,
            'account_id' in payer,
            'account_id' in receiver,
        ]

        if not all(rules):
            return Response('Both payer and receiver should have client_id and account_id', mimetype='text/plain', status=400)

        if 'amount' not in payer:
            return Response('Payer should have an amount to transfer', mimetype='text/plain', status=400)

        return func(*args, **kwargs)
    return validate_params

