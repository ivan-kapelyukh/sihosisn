from flask import Flask
from flask import render_template
from flask import request
import os
import time
import historical as hs
import pandas as pd
import sell_time as st
import requests
import json
from pymongo import MongoClient
from mongoengine import connect
from models.transaction import Transaction
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask_cors import CORS
import numpy as np
import math

from transferwise import TransferWise

# Environment variables
API_TOKEN = os.getenv("TRANSFERWISE_API_TOKEN")
SANDBOX_MODE = os.getenv("TRANSFERWISE_SANDBOX_MODE") == "1"

app = Flask(__name__, template_folder="www")
app.config[
    'MONGO_URI'] = "mongodb://hc4:pgmyzcik99>@ds161724.mlab.com:61724/hc4"

app.config['MONGODB_SETTINGS'] = {'db': 'testing', 'alias': 'default'}

CORS(app)

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
USDJPY["time"] = np.arange(0, len(USDJPY))

EURUSD = pd.read_csv("./data/EURUSD.csv")
EURUSD["time"] = np.arange(0, len(EURUSD))

GBPUSD = pd.read_csv("./data/GBPUSD.csv")
GBPUSD["time"] = np.arange(0, len(GBPUSD))

EURJPY = pd.read_csv("./data/EURJPY.csv")
EURJPY["time"] = np.arange(0, len(EURJPY))

GBPJPY = pd.read_csv("./data/GBPJPY.csv")
GBPJPY["time"] = np.arange(0, len(GBPJPY))

EURGBP = pd.read_csv("./data/EURGBP.csv")
EURGBP["time"] = np.arange(0, len(EURGBP))


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


@app.route("/api/history")
def history():
    source = request.args.get('source')
    target = request.args.get('target')
    time_now = int(request.args.get('time'))

    history = get_history(source, target, time_now - 102 * 60 * 60, time_now)

    print(history)

    return json.dumps(history)


@app.route("/api/transfer")
def transfer():
    source = request.args.get('source')
    target = request.args.get('target')
    amount = request.args.get('amount')
    timeframe = int(request.args.get('timeFrame'))
    # risk = int(request.args.get('risk'))
    demo_mode = request.args.get('demoMode')

    if demo_mode:
        time_now = int(request.args.get('time'))
    else:
        time_now = time.time()

    return save_transaction({
        'source': source,
        'target': target,
        'amount': amount,
        'start': time_now,
        'risk': -1,
        'end': time_now + timeframe,
        'demoMode': demo_mode,
        'amountLeft': amount
    })['id']


@app.route("/api/demo-update")
def demo_update():
    transfer_id = request.args.get('transferId')
    time_elapsed = int(request.args.get('timeElapsed'))

    transaction = get_demo_transfer(transfer_id)['transaction']

    time_now = transaction['start'] + time_elapsed

    transaction_timeframe = transaction['end'] - transaction['start']

    # print(transaction_timeframe)
    print(time_now - transaction_timeframe)
    print(time_now)

    rates = get_history(transaction['source'], transaction['target'],
                            time_now - transaction_timeframe, time_now)

    if transaction['amountLeft'] < 0.1:

        frac = st.fraction_to_sell(transaction['start'], time_now,
                                   transaction['end'], rates,
                                   transaction['end'] - transaction['start'])

        sell_amount = math.floor(
            frac * transaction['amountLeft'] * 100) / 100.0

        print("================")
        print("TRANS AMOUNT LEFT", transaction['amountLeft'])
        print("================")
        print("================")
        print("SELL AMOUNT", sell_amount)
        print("================")

        updateAmountLeft(transfer_id,
                         max(0, transaction['amountLeft'] - sell_amount))

    last_price = rates[-1]

    return json.dumps({
        'price': last_price,
        'soldAmount': sell_amount,
        'boughtAmount': round(sell_amount * last_price, 2)
    })


def updateAmountLeft(transfer_id, new_amount):
    req = requests.post(
        "http://localhost:3001/api/updateTransactionAmount",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "id": transfer_id,
            "amountLeft": new_amount
        }))


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
        headers={"Content-Type": "application/json"},
        data=json.dumps(transaction))

    print("Reached here")
    return req.json()


def add_demo_mode_transfer(source, target, timeframe, risk, demo_mode):
    # TODO: ADD TO DEMO DATABASE :)
    return id


def get_demo_transfer(id):
    print(id)
    temp = {}
    temp["id"] = id
    req = requests.post(
        "http://localhost:3001/api/findTransaction",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "id": id
        }))

    return req.json()


if __name__ == "__main__":
    app.run(debug=True)

save_transaction("test")
