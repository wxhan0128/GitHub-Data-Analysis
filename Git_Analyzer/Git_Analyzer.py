from flask import Flask, render_template, request, redirect, url_for, jsonify
from config import config
from flask_pymongo import PyMongo
import requests
import json
from urllib.parse import urljoin
from datetime import date

app = Flask(__name__, static_folder="./templates/static/dist", template_folder="./templates/static")
app.config.from_object(config["development"])
mongo = PyMongo(app)
GITHUB_API = 'https://api.github.com'


@app.route("/gaz")
def index():
    return render_template("index.html")


@app.route('/gaz/hello')
def hello_world():
    return "Hello World!"


@app.route('/gaz/api/v1.0/repositories', methods=['GET'])
def get_repos():
    try:
        # filter the fields which we want to analyze
        all_repos = mongo.db.repos.find({}, {"id": 1, "name": 1, "description": 1})

        repos_list = []

        for repos in all_repos:
            repos_item = {
                'id': repos['id'],
                'name': repos['name'],
                'description': repos['description'],
            }
            repos_list.append(repos_item)
    except Exception as e:
        return str(e)

    return jsonify(repos_list)


@app.route('/gaz/api/v1.0/top_repositories', methods=['GET'])
def get_top_repos():
    top_repos = mongo.db.repos.find({}, {"id": 1, "name": 1, "stargazers_count": 1}).sort(
        [("stargazers_count", -1)]).limit(100)

    print(top_repos)

    repos_list = []

    for repos in top_repos:
        repos_item = {
            'id': repos['id'],
            'name': repos['name'],
            'star_num': repos['stargazers_count']
        }

        repos_list.append(repos_item)

    return jsonify(repos_list)


@app.route('/gaz/api/v1.0/languages', methods=['GET'])
def get_langs():
    try:
        all_langs = mongo.db.repos.aggregate([
            {
                "$group": {
                    "_id": "$language",
                    "total": {"$sum": 1}
                }
            },
            {
                "$sort": {"total": -1}
            }
        ])

        lang_list = []

        for lang in all_langs:
            lang_item = {
                'language': lang['_id'],
                'total': lang['total']
            }
            lang_list.append(lang_item)
    except Exception as e:
        return str(e)

    return jsonify(lang_list)


@app.route('/gaz/api/v1.0/language_trends', methods=['POST'])
def get_lang_trend():
    lang_name = request.json['lname']
    print(lang_name)

    lang_trend = mongo.db.repos.aggregate(
        [
            {"$match": {"language": lang_name}
             },
            {
                "$group":
                    {
                        "_id": {
                            "year": {"$substr": ["$created_at", 0, 4]},
                            "month": {"$substr": ["$created_at", 5, 2]},
                            "language": "$language",
                        },
                        "count": {"$sum": 1}
                    },
            },
            {"$sort": {"_id.year": 1, "_id.month": 1}},
            {"$project": {"_id": 0, "l": "$_id.language", "y": "$_id.year", "m": "$_id.month", "c": "$count"}}
        ]
    )

    trend_list = []

    for trend in lang_trend:
        trend_item = {
            'language': trend['l'],
            'date': trend['y'] + "-" + trend['m'],
            'total': trend['c']
        }
        trend_list.append(trend_item)

    return jsonify(trend_list)


@app.route('/gaz/api/v1.0/users', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']

    repos_data = get_userRepos(username, password)
    for i in repos_data:
        print(i)
    return jsonify(repos_data)


def get_userRepos(username, password):
    url = urljoin(GITHUB_API, 'user/repos')
    response = requests.get(
        url,
        auth=(username, password),
        params={"affiliation": "owner"}
    )

    if response.ok:
        repos_data = json.loads(response.text or response.content)

        return repos_data
    else:
        print(json.dumps(response.json()['message'], indent=4))


if __name__ == '__main__':
    app.run()
