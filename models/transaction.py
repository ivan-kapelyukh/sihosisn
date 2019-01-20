import mongoengine as me

# see devpost for details on multi-server architecture using Mongo
class Transaction(me.Document):
    transaction = me.StringField(required=True)
