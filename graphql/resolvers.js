const MongoClient = require('mongodb').MongoClient;
var ObjectId = require('mongodb').ObjectID;
const assert = require('assert');

// Connection URL
const url = 'mongodb://root:example@mongodb:27017';

// Database Name
const dbName = 'mail_db';

// Create a new MongoClient
const client = new MongoClient(url, {useUnifiedTopology: true});

const findDocuments = function (db, col, query, callback) 
{
    // Get the documents collection
    const collection = db.collection(col);
    // Find some documents
    collection.find(query).toArray(function (err, docs) {
        assert.equal(err, null);
        callback(docs);
    });
}

const countDocuments = function (db, col, query, callback) 
{
    // Get the documents collection
    const collection = db.collection(col);
    // Find some documents
    collection.countDocuments(query, function (err, docs) {
        assert.equal(err, null);
        callback(docs);
    });
}

const distinctDocuments = function (db, col, query, callback) 
{
    // Get the documents collection
    const collection = db.collection(col);
    // Find some documents
    collection.distinct(query, function (err, docs) {
        assert.equal(err, null);
        callback(docs);
    });
}

const aggregateDocuments = function (db, col, query, callback) 
{
    // Get the documents collection
    const collection = db.collection(col);
    // Find some documents
    collection.aggregate(query).toArray( function (err, docs) {
        assert.equal(err, null);
        callback(docs);
    });
}



client.connect(function (err) {
    assert.equal(err, null);
    console.log("Connected correctly to the MongoDB server");
});


// un résolveur simple pour la requête 'books' de type Query
// qui renvoie la variable 'books'
const resolvers = {
    Query: {
        CountItem(root, args, context) 
        {
            return new Promise((resolve, reject) => {
                const db = client.db(dbName);
                countDocuments(db, 'mail', {}, resolve);
            }).then(result => {
                return result;
            });
        },
        Mails(root, args, context) 
        {
            return new Promise((resolve, reject) => {
                const db = client.db(dbName);
                findDocuments(db, 'mail', {}, resolve);
            }).then(result => {
                return result;
            });
        },
        Distinct(root, args, context) 
        {
            return new Promise((resolve, reject) => {
                const db = client.db(dbName);
                distinctDocuments(db, 'mail', 'labels' , resolve);
            }).then(result => {
                return result;
            });
        },
        CountDistinct(root, args, context) 
        {
            query = [{ $unwind: "$labels" },
                { $group: { "_id": "$labels.name", "count": { $sum: 1 } } }, 
                { $project: { "_id": 0, "name": "$_id", "count": 1 } },
                { $sort : { count : -1} }];
            return new Promise((resolve, reject) => {
                const db = client.db(dbName);
                aggregateDocuments(db, 'mail', query , resolve);
            }).then(result => {
                return result;
            });
        },
        SumCountDistinct(root, args, context) 
        {
            query = [{ $unwind: "$labels" },
                { $group: { "_id": "$labels.name", "count": { $sum: 
                            { '$toInt': '$labels.count' } } } }, 
                { $project: { "_id": 0, "name": "$_id", "count": 1 } },
                { $sort : { count : -1} }];
            return new Promise((resolve, reject) => {
                const db = client.db(dbName);
                aggregateDocuments(db, 'mail', query , resolve);
            }).then(result => {
                return result;
            });
        },
        MailByAllLabel(root, args, context) 
        {
            query = { "labels.name": 
                { $all: args.labelChoosed }}, 
                {_id:1, date:1};
            return new Promise((resolve, reject) => {
                const db = client.db(dbName);
                findDocuments(db, 'mail', query , resolve);
            }).then(result => {
                return result;
            });
        },
        MailByInLabel(root, args, context) 
        {
            query = { "labels.name": 
                { $in: args.labelChoosed }}, 
                {_id:1, date:1};
            return new Promise((resolve, reject) => {
                const db = client.db(dbName);
                findDocuments(db, 'mail', query , resolve);
            }).then(result => {
                return result;
            });
        },
    }
};

// on exporte la définition de 'resolvers'
module.exports = resolvers;
