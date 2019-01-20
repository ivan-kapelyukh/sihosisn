const mongoose = require("mongoose");
const express = require("express");
const bodyParser = require("body-parser");
const logger = require("morgan");

const Transaction = require("./models/transaction");

const API_PORT = 3001;
const app = express();
const router = express.Router();

var ObjectId = mongoose.Types.ObjectId;

const dbRoute = "mongodb://my1817:my1817@ds161724.mlab.com:61724/hc4test";


mongoose.connect(
    dbRoute,
    { useNewUrlParser: true }
);

let db = mongoose.connection;

db.once("open", () => console.log("connected to the database"));

// checks if connection with the database is successful
db.on("error", console.error.bind(console, "MongoDB connection error:"));

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(logger("dev"));
app.use(function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

router.post("/saveTransaction", (req, res) => {
    let transaction = new Transaction();

    console.log(req.body);

    transaction.source = req.body.source;
    transaction.target = req.body.target;
    transaction.amount = req.body.amount;
    transaction.start = req.body.start;
    transaction.end = req.body.end;
    transaction.risk = req.body.risk;
    transaction.demoMode = req.body.demoMode;
    transaction.amountLeft = req.body.amountLeft;

    transaction.save((err, data) => {
        if (err) {
            return res.json({ success: false, err: err });
        } else {
            return res.json({ success: true, id: data._id });
        }
    })
})

router.post("/findTransaction", (req, res) => {

    Transaction.findOne(
        { _id: ObjectId(req.body.id) },
        (error, data) => {
            if (error) {
                return res.json({ success: false, error: error });
            } else {
                return res.json({ success: true, transaction: data });
            }
        });
})

router.post("/updateTransactionAmount", (req, res) => {

    var amountLeft = req.body.amountLeft;

    Transaction.findOneAndUpdate(
        { _id: ObjectId(req.body.id) },
        { $set: { "amountLeft": amountLeft } },
        (error, data) => {
            if (error) {
                console.log(data);
                return res.json({ success: false, error: error });
            } else {
                console.log(data);
                return res.json({ success: true, transaction: data });
            }
        });
})


app.use("/api", router);
app.listen(API_PORT, () => console.log(`LISTENING ON PORT ${API_PORT}`));
