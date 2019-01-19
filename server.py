from flask import Flask
from flask import render_template
from flask import request
import os
import time
import historical as hs
import sell_time as st
import json

from transferwise import TransferWise

# Environment variables
API_TOKEN = os.getenv("TRANSFERWISE_API_TOKEN")
SANDBOX_MODE = os.getenv("TRANSFERWISE_SANDBOX_MODE") == "1"

app = Flask(__name__, template_folder="www")

tw_handler = TransferWise(API_TOKEN, SANDBOX_MODE)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/profiles")
def profiles():
    return tw_handler.get_profiles()


# @app.route("/quote")
# def quote():
#     profile = request.args.get('profile')
#     source = request.args.get('source')
#     target = request.args.get('target')
#     rate_type = request.args.get('rate')
#     target_amount = request.args.get('amount')
#     payment_type = request.args.get('type')
#     return tw_handler.create_quote(profile, source, target, rate_type,
#                                    target_amount, payment_type)


def demo_transfer(source, target, start_time, end_time, risk):
    for t in range(start_time, end_time, 24 * 60 * 60):

        past_data = hs.get_gpb_usd_historical(t - 30 * 24 * 60 * 60, t)

        # return past_data

        if st.should_sell(t, end_time, past_data):
            return t

    return end_time


def add_transfer(source, target, start_time, end_time, risk):
    # Adds transfer to database
    return


def query_transfer(past_data, current_quote, transfer):
    # Queries all awaiting transfers and detemine what to do for each
    if (transfer_now(past_data, current_quote, transfer)):
        # TODO: Transfer
        return True

    return False


def transfer_now(past_data, current_quote, transfer):
    return True


@app.route("/transfer", methods=["POST"])
def transfer():
    source = request.form.get('source')
    target = request.form.get('target')
    timeframe = int(request.form.get('timeframe'))
    risk = request.form.get('risk')
    demo_mode = request.form.get('demoMode')

    if demo_mode:
        ts = int(request.form.get('time'))
        return str(demo_transfer(source, target, ts, ts + timeframe, risk))
    else:
        ts = time.time()
        add_transfer(source, target, ts, ts + timeframe, risk)

    return json.dumps({
        'success': True,
        'source': source,
        'target': target,
        'timeframe': timeframe,
        'risk': risk,
        'demoMode': demo_mode
    })


# @app.route("/recipient")
# def recipient():
#     currency = request.args.get('currency')
#     recipient_type = request.args.get('type')
#     profile = request.args.get('profile')
#     name = request.args.get('name')
#     legal_type = request.args.get('legal_type')
#     sort_code = request.args.get('sort_code')
#     acc_no = request.args.get('acc_no')
#     return tw_handler.create_recipient_account()

if __name__ == "__main__":
    app.run(debug=True)
