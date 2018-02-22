from data_fetching import DataFetching
from pymongo import MongoClient
import json


class DataStoring:
    def __init__(self, git_username, git_password, token, mongo_username, mongo_password):
        self.token = token
        self.df = DataFetching(git_username, git_password)

        self.mongo_uri = 'mongodb://%s:%s@cluster0-shard-00-01-i6gcp.mongodb.net:27017/admin' % (
            mongo_username, mongo_password)
        self.client = MongoClient(self.mongo_uri,
                                  ssl=True,
                                  replicaSet='Cluster0-shard-0',
                                  authSource='admin')
        print(self.client)
        # client = MongoClient(
        #     "mongodb://Campione:veTRxJL29lpKWwPn@cluster0-shard-00-01-i6gcp.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")

    def insert_repositories(self, times):
        db = self.client.gitdb
        repos_collection = db.repos

        since = 0
        for i in range(0, times):
            response = self.df.get_all_repositories(self.token, since)
            if response.ok:
                repos_data = json.loads(response.text or response.content)
                # for repos in repos_data:
                repos_collection.insert_many(repos_data)

                since = repos_data[-1]["id"]
            else:
                print()

        return repos_collection

    def insert_users(self):
        pass


if __name__ == '__main__':
    git_username = input('GitHub username: ')
    git_password = input('GitHub password: ')
    token = 'your token'

    # the mongodb user name and a random password for our cluster
    ds = DataStoring(git_username, git_password, token, 'mongodb username', 'mongodb password')
    print(ds.insert_repositories(1).count())
