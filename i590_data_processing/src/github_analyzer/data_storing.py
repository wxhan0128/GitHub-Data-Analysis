from data_fetching import DataFetching
from pymongo import MongoClient
import pymongo
from pymongo.errors import ConnectionFailure
import win_unicode_console


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

        try:
            info = self.client.server_info()  # Forces a call.
            print(info)
            print(self.client.database_names())
        except ConnectionFailure:
            print('Failed to connect to server: %s' % self.mongo_uri)
            exit()

        # client = MongoClient(
        #     "mongodb://Campione:veTRxJL29lpKWwPn@cluster0-shard-00-01-i6gcp.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")

    def build_index(self):
        db = self.client.gitdbPro
        db.repos.create_index([('id', pymongo.ASCENDING)], unique=True)
        sorted(list(db.repos.index_information()))

    def insert_repositories(self, since, times):
        db = self.client.gitdbPro
        repos_collection = db.repos

        entry = since
        list = []  # move all data into a list and do batch insert
        for i in range(0, times):
            all_repos = self.df.get_all_repositories(self.token, entry)
            if all_repos != 'request error':  # the input might be invalid
                for repos in all_repos:
                    detail = self.df.get_repository_details(self.token, repos['url'])
                    if detail != 'not found':  # some urls of the repository cannot be visited
                        list.append(detail)
                        # repos_collection.insert(detail)

                entry = all_repos[-1]['id']
            else:
                break

        repos_collection.insert_many(list)
        list.clear()
        self.client.close()

        return entry, repos_collection

    def insert_latest_repositories(self, total_pages):
        db = self.client.gitdbPro
        repos_collection = db.repos

        for i in range(0, total_pages):
            all_latest_repos = self.df.search_latest_repositories(self.token, i)
            if all_latest_repos != 'request error':
                # for repos in all_latest_repos:
                repos_collection.insert_many(all_latest_repos['items'])
            else:
                break

        self.client.close()

        return repos_collection

    def insert_star_repositories(self, year, month, stars):
        db = self.client.gitdbPro
        repos_collection = db.repos

        for i in range(1, 32):
            all_star_repos = self.df.search_star_repositories(self.token, year, month, i, stars)
            if all_star_repos != 'request error' and all_star_repos != 'date invalid':
                print('day: %d, search number: %d' % (i, all_star_repos['total_count']))
                repos_collection.insert_many(all_star_repos['items'])
            else:
                break

        self.client.close()


if __name__ == '__main__':
    git_username = input('GitHub username: ')
    git_password = input('GitHub password: ')
    # git_password = getpass.getpass('GitHub password: ')
    token = '85015b14f0ff000b5ace4789c0de0e6a9f4c39b6'

    # win_unicode_console.enable()
    # the mongodb user name and a random password for our cluster
    ds = DataStoring(git_username, git_password, token, 'Campione', 'veTRxJL29lpKWwPn')
    # ds.build_index()
    # total: 25680

    # last_since, repos_collection = ds.insert_repositories(115969606, 100)
    #
    # print(repos_collection.count())
    # print(last_since)
    ds.insert_star_repositories(2018, 1, 40)
