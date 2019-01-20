import mongoengine as me


class Transaction(me.Document):
    transaction = me.StringField(required=True)
