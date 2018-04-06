import requests
import json
from urllib.parse import urljoin
from pymongo import MongoClient
import pymongo
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId


class GetLanguages:
    def __init__(self, mongo_username, mongo_password):
        self.GITHUB_API = 'https://api.github.com'  # basic api address
        self.mongo_uri = 'mongodb://%s:%s@cluster0-shard-00-01-i6gcp.mongodb.net:27017/admin' % (
            mongo_username, mongo_password)
        self.client = MongoClient(self.mongo_uri,
                                  ssl=True,
                                  replicaSet='Cluster0-shard-0',
                                  authSource='admin')

        try:
            info = self.client.server_info()  # Forces a call.
            print(info)
            print(self.client.database_names())
        except ConnectionFailure:
            print('Failed to connect to server: %s' % self.mongo_uri)
            exit()

    def read_lang_url(self, objectId):
        db = self.client.gitdbPro
        repos = db.repos
        record = repos.find_one({'_id': ObjectId(objectId)})
        print(record['languages_url'])
        return record['languages_url']




    def get_languages(self, token, repo):
        #get_lang_url = urljoin(self.GITHUB_API, '/repos/' + repo)
        head = {'Authorization': 'token %s' % token}
        response = requests.get(
    		repo,
    		headers=head
    	)
        if response.ok:
            languages = json.loads(response.text or response.content)
            return languages
        else:
            print(json.dumps(response.json()['message'], indent=4))
            error = 'request error'
            return error

    def test_iteration(self):
        db = self.client.gitdbPro
        repos = db.repos
        #print(repos.count())
        for repo in repos.find().limit(5):
            #print(repo['full_name'])

            print(repo['_id'])

    def store_langs(self, start_id):
        db = self.client.gitdbPro
        repos = db.repos
        langs = db.langs
        list = []
        end = start_id
        for repo in repos.find({'_id': {'$gt':ObjectId(start_id)}}).limit(56):
            lang_url = self.read_lang_url(repo['_id'])
            langs = self.get_languages(token, lang_url)
            #print(repo['_id'])
            #print(langs)
            if (langs != 'reques error' and langs!="Not Found" and langs != "Server Error"):
                origin_id = ObjectId(repo['_id'])
                data = {
                    '_id':origin_id,
                    'id': repo['id'],
                    'languages':langs
                }
                #print(json.dumps(data))
                list.append(data)
                end = repo['_id']
            else:
                end = repo['_id']
                print("Error!!!")
                break
        print(end)
        try:
            db.langs.insert_many(list)
            self.client.close()
        except ConnectionFailure:
            print('Failed to insert documents into %s' % langs)
            exit()

    def test_compare_id(self, start_id):
        db = self.client.gitdbPro
        repos = db.repos
        langs = db.langs
        list = []
        for repo in repos.find({'_id': {'$gt':ObjectId(start_id)}}).limit(4000):
            print(repo)


if __name__ == '__main__':

    gl = GetLanguages('Campione', 'veTRxJL29lpKWwPn')
    token = '85015b14f0ff000b5ace4789c0de0e6a9f4c39b6'

    # Call function to get languages data for each repository
    #searched_data = gl.get_languages(token, "kelseyhightower/echo/languages")
    #if searched_data != 'request error' and searched_data != 'date invalid':
     #       print(searched_data)

    # Get language url
    #lang_url = gl.read_lang_url("5abe9b96c44bb82d0c83b3ae")
    #langs = gl.get_languages(token, lang_url)
    #print(langs)

    # Test collection iteration
    #gl.test_iteration()

    # Test data storing
    start_id = "5abead73c44bb85a98c83358"
    gl.store_langs(start_id)

    # Test start id search
    #start_id = "5abe9b96c44bb82d0c83b394"
    #gl.test_compare_id(start_id)

