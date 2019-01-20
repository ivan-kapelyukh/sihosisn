from flask import Flask
from flask import render_template
from flask import request

from models.transaction import Transaction
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient

app = Flask(__name__, template_folder="www")

app.config['MONGO_DBNAME'] = 'hc4'  # name of database on mongo
app.config[
    "MONGO_URI"] = "mongodb://my1817:my1817@ds161724.mlab.com:61724/hc4test"
mongo = PyMongo(app)


@app.route("/save")
def save():
    save_transaction("hello")


def save_transaction(transaction):
    trans = Transaction(transaction)
    trans.save()


if __name__ == "__main__":
    app.run(debug=True)
