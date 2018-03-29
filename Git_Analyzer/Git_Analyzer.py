from flask import Flask, render_template, request, redirect, url_for, jsonify
from config import config

app = Flask(__name__)
app.config.from_object(config["development"])
client = config["development"].client
db = client.gitdbPro # test


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/gaz/api/v1.0/repositories', methods=['GET'])
def get_repos():
    try:
        all_repos = db.repos.find({})
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

    # return render_template('test_page01.html', alldata=repos_data, t=title, h=heading)
    return jsonify(repos_list)


@app.route('/gaz/api/v1.0/languages', methods=['GET'])
def get_langs():
    try:
        all_langs = db.repos.aggregate([
            {
                "$group": {
                    "_id": "$language",
                    "total": {"$sum": 1}
                }
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

    # return render_template('test_page02.html', alldata=all_langs, t=title, h=heading)


if __name__ == '__main__':
    app.run()
