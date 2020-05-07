import json
import os

import plaid
from flask import Flask
from flask import jsonify
from flask import request
# from dotenv import load_dotenv

app = Flask(__name__)
# load_dotenv()

PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_PUBLIC_KEY = os.getenv('PLAID_PUBLIC_KEY')
PLAID_ENV = os.getenv('PLAID_ENV')
PLAID_PRODUCTS = os.getenv('PLAID_PRODUCTS')
PLAID_COUNTRY_CODES = os.getenv('PLAID_COUNTRY_CODES')

ACCESS_TOKENS = os.getenv('PLAID_ACCESS_TOKENS', '')

client = plaid.Client(
    client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET,
    public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV,
    api_version='2019-05-29',
)

html = '''
<html>
<head>
<title>My Flask Application</title>
</head>
<body>
<h1>This is the Home page!</h1>
</body>
</html>
'''


app.add_url_rule('/', 'index', (lambda: html))


def get_balances(access_token: str):
    """Uses an access token to parse and return basic balance information

    Arguments:
        access_token {str} -- Access token for a given Item

    Returns:
        List -- A list of tuples of (balance dict, account name)
    """
    try:
        balance_response = client.Accounts.balance.get(access_token)
    except plaid.errors.PlaidError as e:
        print(e)
        return

    balances = [{
        'name': account['name'], 'amount': account['balances']['current'],
        'currency': account['balances']['iso_currency_code'],
    } for account in balance_response['accounts']]

    pretty_print_response(balance_response)

    return balances


def pretty_print_response(response):
    print(json.dumps(response, indent=2, sort_keys=True))


@app.route('/get_accounts', methods=['POST'])
def get_accounts():
    tokens = request.form['tokens'].split(',')
    accounts = [balance for token in tokens for balance in get_balances(token)]
    return jsonify(accounts)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
