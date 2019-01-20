from flask import Flask
from flask import render_template
from flask import request

from models.transaction import Transaction
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient
import requests
import json


def get_demo_transfer(id):
    print(id)
    temp = {}
    temp["id"] = id
    print(temp)
    req = requests.post(
        "http://localhost:3001/api/findTransaction",
        headers={"Content-Type": "application/json"},
        data=json.dumps(temp))

    return req.json()


print(get_demo_transfer("5c44323f259a57873fb79543")['transaction'])
# json.dumps({'id': 5c44323f259a57873fb79543})
