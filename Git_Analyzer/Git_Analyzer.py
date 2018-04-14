from flask import Flask, render_template, request, redirect, url_for, jsonify
from config import config
from flask_pymongo import PyMongo

app = Flask(__name__, static_folder="./templates/static/dist", template_folder="./templates/static")
app.config.from_object(config["development"])
mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/hello')
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

    # return render_template('test_page01.html', alldata=all_repos, t=title, h=heading)
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

    # return render_template('test_page02.html', alldata=all_langs, t=title, h=heading)
    return jsonify(lang_list)


if __name__ == '__main__':
    app.run()
