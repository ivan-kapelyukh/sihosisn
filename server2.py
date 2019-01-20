from flask import Flask
from flask import render_template
from flask import request
import os
import time
import historical as hs
import pandas as pd
# import sell_time as st
import json
from pymongo import MongoClient
from mongoengine import connect
from models.transaction import Transaction
from bson.objectid import ObjectId
from flask_pymongo import PyMongo

from transferwise import TransferWise

# Environment variables
API_TOKEN = os.getenv("TRANSFERWISE_API_TOKEN")
SANDBOX_MODE = os.getenv("TRANSFERWISE_SANDBOX_MODE") == "1"

app = Flask(__name__, template_folder="www")
app.config[
    'MONGO_URI'] = "mongodb://hc4:pgmyzcik99>@ds161724.mlab.com:61724/hc4"

app.config['MONGODB_SETTINGS'] = {'db': 'testing', 'alias': 'default'}
mongo = PyMongo(app)

# DB_NAME = "hc4"
# DB_HOST = "s161724.mlab.com"
# DB_PORT = 61724
# DB_USER = "hc4"
# DB_PASS = "pgmyzcik99"

# connection = MongoClient(DB_HOST, DB_PORT)
# db = connection[DB_NAME]
# db.authenticate(DB_USER, DB_PASS)

tw_handler = TransferWise(API_TOKEN, SANDBOX_MODE)


@app.route("/")
def index():
    return render_template('index.html')


USDJPY = pd.read_csv("./data/USDJPY.csv")

EURUSD = pd.read_csv("./data/EURUSD.csv")

GBPUSD = pd.read_csv("./data/GBPUSD.csv")

EURJPY = pd.read_csv("./data/EURJPY.csv")

GBPJPY = pd.read_csv("./data/GBPJPY.csv")

EURGBP = pd.read_csv("./data/EURGBP.csv")


def get_range(data, x, y):
    return data[(x < data["time"]) & (data["time"] < y)]["close"].tolist()


def invert(list):
    return [1 / x for x in list]


def get_history(src, trg, start, end):

    if src == "USD":
        if trg == "JPY":
            return get_range(USDJPY, start, end)
        elif trg == "EUR":
            return invert(get_range(EURUSD, start, end))
        elif trg == "GBP":
            return invert(get_range(GBPUSD, start, end))

    elif src == "JPY":
        if trg == "USD":
            return invert(get_range(USDJPY, start, end))
        elif trg == "EUR":
            return invert(get_range(EURJPY, start, end))
        elif trg == "GBP":
            return invert(get_range(GBPJPY, start, end))

    elif src == "EUR":
        if trg == "USD":
            return get_range(EURUSD, start, end)
        elif trg == "JPY":
            return get_range(EURJPY, start, end)
        elif trg == "GBP":
            return get_range(EURGBP, start, end)

    elif src == "GBP":
        if trg == "USD":
            return get_range(GBPUSD, start, end)
        elif trg == "JPY":
            return get_range(GBPJPY, start, end)
        elif trg == "EUR":
            return invert(get_range(EURGBP, start, end))


@app.route("/history")
def history():
    source = request.args.get('source')
    target = request.args.get('target')
    time_now = int(request.args.get('time'))

    history = get_history(source, target, time_now - 100 * 60 * 60, time_now)

    print(history)

    return json.dumps(history)  # TODO: list of normalized history


@app.route("/demo-update")
def demo_update():
    transfer_id = request.args.get('transferId')
    time = request.args.get('time')

    transaction = get_demo_transfer(transfer_id).transaction

    return json.dumps({
        'price': -1,
        'sell_amount': 0,
    })


@app.route("/transfer", methods=["POST"])
def transfer():
    source = request.form.get('source')
    target = request.form.get('target')
    amount = request.form.get('amount')
    timeframe = int(request.form.get('timeFrame'))
    risk = int(request.form.get('risk'))
    demo_mode = request.form.get('demoMode')

    return save_transaction({
        'source': source,
        'target': target,
        'amount': amount,
        'start': time,
        'end': time + timeframe,
        'demoMode': demo_mode
    })


@app.route("/price")
def price():
    src = request.args.get('source')
    trg = request.args.get('target')

    demo_mode = request.form.get('demoMode')

    return  # close value


@app.route("/transaction")
def transaction():
    transaction_id = request.args.get('id')


@app.route("/save")
def save():
    save_transaction("hello")


def save_transaction(transaction):
    req = requests.post(
        "http://localhost:3001/api/saveTransaction",
        headers={
            "Authorization": "Bearer {}".format(self.api_token),
            "X-idempotence-uuid":
            str(uuid.uuid4()),  # Only used for borderless conversions
            "Content-Type": "application/json"
        },
        data=transaction)

    return req.json()


def add_demo_mode_transfer(source, target, timeframe, risk, demo_mode):
    # TODO: ADD TO DEMO DATABASE :)
    return id


def get_demo_transfer(id):
    req = requests.post(
        "http://localhost:3001/api/findTransaction",
        headers={
            "Authorization": "Bearer {}".format(self.api_token),
            "X-idempotence-uuid":
            str(uuid.uuid4()),  # Only used for borderless conversions
            "Content-Type": "application/json"
        },
        data=transaction_id)

    return req.json()


if __name__ == "__main__":
    app.run(debug=True)

save_transaction("test")
