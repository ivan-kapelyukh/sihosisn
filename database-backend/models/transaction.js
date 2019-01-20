const mongoose = require("mongoose");
const Schema = mongoose.Schema;


const TransactionSchema = new Schema(
    {
        source: { type: String, required: true },
        target: { type: String, required: true },
        amount: { type: Number, required: true },
        start: { type: Number, required: true },
        end: { type: Number, required: true },
        risk: { type: Number, required: true },
        demoMode: { type: String, required: true },
        amountLeft: { type: Number, required: true }
    }
);

module.exports = mongoose.model("Transaction", TransactionSchema);
