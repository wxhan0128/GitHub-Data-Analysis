from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import pymongo
from pymongo.errors import ConnectionFailure

mongo_uri = 'mongodb://%s:%s@cluster0-shard-00-01-i6gcp.mongodb.net:27017/admin' % (
    'Campione', 'veTRxJL29lpKWwPn')
client = MongoClient(mongo_uri,
                     ssl=True,
                     replicaSet='Cluster0-shard-0',
                     authSource='admin')

try:
    info = client.server_info()  # Forces a call.
    print(info)
    print(client.database_names())
except ConnectionFailure:
    print('Failed to connect to server: %s' % mongo_uri)
    exit()

db = client.gitdbPro

app = Flask(__name__)
title = "GitHub Data with Flask"
heading = "List all"


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/listAll')
def list_alldata():
    repos_data = db.repos.find({})
    return render_template('test_page01.html', alldata=repos_data, t=title, h=heading)


@app.route('/langs')
def list_langdata():
    langs_data = db.repos.aggregate([
        {
            "$group": {
                "_id": "$language",
                "total": {"$sum": 1}
            }
        }
    ])

    return render_template('test_page02.html', alldata=langs_data, t=title, h=heading)


if __name__ == '__main__':
    app.run()
