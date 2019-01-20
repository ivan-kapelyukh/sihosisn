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

quote = transferwise.create_quote(
    profile_id=profile['id'],
    source="EUR",
    target="USD",
    target_amount=100,
    quote_type="BALANCE_CONVERSION")

# useful for debugging!
print("%s/%s :: %f" % (quote["source"], quote["target"], quote["rate"]))

# transfer_id = 47669084
# transfer = transferwise.get_transfer(transfer_id)

# print("Initial Status :: %s" % (transfer['status']))

# # print(transferwise.fund_transfer(transfer_id))
# # {'type': 'BALANCE', 'status': 'REJECTED', 'errorCode': 'balance.payment-option-unavailable'}

# transferwise.simulate_processing_transfer(transfer_id)
# transferwise.simulate_funds_converted(transfer_id)
# transferwise.simulate_outgoing_payment_sent(transfer_id)

# print("Final Status :: %s" % (transfer['status']))
