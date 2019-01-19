from enum import Enum

import os
import requests
import uuid
import json

# TransferWise Variables
SANDBOX_API = "https://api.sandbox.transferwise.tech/v1/"
LIVE_API = "https://api.transferwise.com/"


class TransferWise:
    def __init__(self, api_token, sandbox_mode):
        self.api_token = api_token
        self.base_url = SANDBOX_API if sandbox_mode else LIVE_API
        self.sandbox_mode = sandbox_mode

    @property
    def headers(self):
        return {
            "Authorization": "Bearer {}".format(self.api_token),
            "X-idempotence-uuid":
            str(uuid.uuid4()),  # Only used for borderless conversions
            "Content-Type": "application/json"
        }

    def get(self, endpoint, params={}):
        req = requests.get(
            self.base_url + endpoint, headers=self.headers, params=params)

        return req.json()

    def post(self, endpoint, data):
        req = requests.post(
            self.base_url + endpoint,
            headers=self.headers,
            data=json.dumps(data))

        return req.json()

    def put(self, endpoint):
        req = requests.put(self.base_url + endpoint, headers=self.headers)

        return req.json()

    # You only need to call this endpoint once to obtain your user profile id.
    # Your personal and business profiles have different IDs.
    # Profile id values are required when making payouts.
    def get_profiles(self):
        return self.get("profiles")

    # Get available balances for all activated currencies in your account.
    def get_account_balance(self, profile_id):
        return self.get(
            "borderless-accounts", params={'profileId': profile_id})

    # Quote fetches current mid-market exchange rate that will be used for your transfer.
    # Quote also calculates our fee and estimated delivery time.
    def create_quote(self, profile_id, source, target, target_amount,
                     quote_type):
        return self.post(
            "quotes", {
                "profile": profile_id,
                "source": source,
                "target": target,
                "rateType": "FIXED",
                "targetAmount": target_amount,
                "type": quote_type
            })

    # Same as create_quote, since temporary quote is not stored and cannot be used for creating transfer.
    # Temporary quote is not associated with any user, it is anonymous.
    def get_temporary_quote(self, profile_id, source, target, target_amount):
        return self.post(
            "quotes", {
                "profile": profile_id,
                "source": source,
                "target": target,
                "rateType": "FIXED",
                "targetAmount": target_amount,
                "type": "BALANCE_PAYOUT"
            })

    # Recipient is a person or institution who is the ultimate beneficiary of your payment.
    def create_recipient_account(self, currency, accountType, legalType,
                                 profile_id, account_holder_name, details):
        return self.post(
            "recipient", {
                "currency": currency,
                "type": type,
                "profile": profile_id,
                "accountHolderName": account_holder_name,
                "legalType": legalType,
                "details": details
            })

    # A transfer is a payout order you make to a recipient account based on a quote.
    # Once created, a transfer will need to be funded within the next 5 working days,
    # or it’ll automatically get cancelled.
    def create_transfer(self, recipient_account_id, quote_id,
                        customer_transaction_id):
        return self.post(
            "transfers", {
                "targetAccount": recipient_account_id,
                "quote": quote_id,
                "customerTransactionId": customer_transaction_id
            })

    # This API call is the final step for executing payouts.
    # TransferWise will now debit funds from your borderless
    # balance and start processing your transfer.
    def fund_transfer(self, transfer_id):
        return self.post("transfers/{}/payments".format(transfer_id),
                         {"type": "BALANCE"})

    def get_transfer(self, transfer_id):
        return self.get("transfers/{}".format(transfer_id))

    # Only transfers which are not funded can be cancelled.
    # Cancellation is final it can not be undone.
    def cancel_transfer(self, transfer_id):
        return self.put("transfers/{}/cancel".format(transfer_id))

    # Fetch a list of your recipient accounts.
    # Use the currency and profile parameters to filter by currency and/or user profile Id.
    def list_recipient_accounts(self, profile_id, currency):
        return self.get(
            "accounts", params={
                "profile": profile_id,
                "currency": currency
            })

    def rates(self):
        return self.get("rates")

    # Fetches list of historical measurements, in form:
    # { "rate": 1.166, "source": "EUR", "target": "USD", "time": "2018-08-31T10:43:31+0000" }
    # Example query: https://api.sandbox.transferwise.tech/v1/rates?source=EUR&target=USD&from=2017-02-13T14:53:01&to=2017-03-13T14:53:01&group=hour
    def get_historical_data(self, source, target, start, end, group):
        return self.get(
            "rates",
            params={
                "source": source,
                "target": target,
                "from": start,
                "to": end,
                "group": group
            })

    # ================== #
    # BORDERLESS ACCOUNT #
    # ================== #

    def get_borderless_accounts(self, profile_id):
        return self.get(
            "borderless-accounts", params={'profileId': profile_id})

    def convert_currencies(self, borderless_account_id, quote_id):
        return self.post(
            "borderless-accounts/{}/conversions".format(borderless_account_id),
            data={"quoteId": quote_id})

    # =================== #
    # TRANSFER SIMULATION #
    # =================== #

    # You can simulate payment processing by changing transfer statuses using these endpoints.
    # This feature is limited to sandbox only.

    # Changes transfer status from incoming_payment_waiting to processing.
    def simulate_processing_transfer(self, transfer_id):
        assert self.sandbox_mode

        return self.get(
            "simulation/transfers/{}/processing".format(transfer_id))

    # Changes transfer status from processing to funds_converted.
    def simulate_funds_converted(self, transfer_id):
        assert self.sandbox_mode

        return self.get(
            "simulation/transfers/{}/funds_converted".format(transfer_id))

    # Changes transfer status from funds_converted to outgoing_payment_sent.
    def simulate_outgoing_payment_sent(self, transfer_id):
        assert self.sandbox_mode

        return self.get("simulation/transfers/{}/outgoing_payment_sent".format(
            transfer_id))

    # Changes transfer status from outgoing_payment_sent to bounced_back.
    def simulate_bounced_back(self, transfer_id):
        assert self.sandbox_mode

        return self.get(
            "simulation/transfers/{}/bounced_back".format(transfer_id))

    # Changes transfer status from bounced_back to funds_refunded
    def simulate_funds_refunded(self, transfer_id):
        assert self.sandbox_mode

        return self.get(
            "simulation/transfers/{}/funds_refunded".format(transfer_id))
