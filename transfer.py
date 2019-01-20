from dotenv import load_dotenv
load_dotenv()

import os
import uuid

from transferwise import TransferWise
from transferwise import types

# Environment variables
API_TOKEN = os.getenv("TRANSFERWISE_API_TOKEN")
SANDBOX_MODE = os.getenv("TRANSFERWISE_SANDBOX_MODE")

transferwise = TransferWise(API_TOKEN, SANDBOX_MODE)

profile = transferwise.get_profiles()[0]


def print_balances():
    balances = transferwise.get_account_balance(profile['id'])[0]['balances']

    for balanceData in balances:
        print(balanceData['currency'] + " :: " +
              str(balanceData['amount']['value']))


def print_quote(quote):
    print("QUOTE: %s/%s" % (quote['source'], quote['target']))
    print("Rate :: %f" % (quote['rate']))
    print("Fee :: %.2f" % (quote['fee']))

    print("%.2f %s => %.2f %s" % (quote['sourceAmount'], quote['source'],
                                  quote['targetAmount'], quote['target']))

# Set up initial data
print("INITIAL BALANCES")
print_balances()
print("====================")

quote = transferwise.create_quote(
    profile_id=profile['id'],
    source="EUR",
    target="GBP",
    target_amount=100,
    quote_type="BALANCE_CONVERSION")

print_quote(quote)
print("====================")

borderless_account = transferwise.get_borderless_accounts(
    profile_id=profile['id'])[0]

transfer = transferwise.convert_currencies(borderless_account['id'],
                                           quote['id'])

print("FINAL BALANCES")
print_balances()
print("====================")

# recipient_account_id = transferwise.list_recipient_accounts(
#     profile['id'], quote['target'])[0]['id']

# transfer = transferwise.create_transfer(
#     recipient_account_id=recipient_account_id,
#     quote_id=quote['id'],
#     customer_transaction_id=str(uuid.uuid4()))

# print("TRANSFER CREATED:")
# print("ID :: %s" % (transfer['id']))

# print("------------------")

# transfer_id = transfer['id']

# transferwise.simulate_processing_transfer(transfer_id)
# transferwise.simulate_funds_converted(transfer_id)
# transferwise.simulate_outgoing_payment_sent(transfer_id)

# transfer = transferwise.get_transfer(transfer_id)

# print("Final Status :: %s" % (transfer['status']))
