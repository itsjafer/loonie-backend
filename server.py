import json
import os

import plaid
from dotenv import load_dotenv

load_dotenv()

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

    balances = [(account['balances'], account['name'])
                for account in balance_response['accounts']]

    pretty_print_response(balance_response)

    return balances


def pretty_print_response(response):
    print(json.dumps(response, indent=2, sort_keys=True))


if __name__ == "__main__":

    access_tokens = ACCESS_TOKENS.split(',')
    accounts = [get_balances(token) for token in access_tokens]
