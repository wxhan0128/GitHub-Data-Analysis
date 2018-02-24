from data_fetching import DataFetching
from pymongo import MongoClient
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
        print(self.client)

    def insert_repositories(self, since, times):
        db = self.client.gitdb
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

        return repos_collection

    def insert_latest_repositories(self, total_pages):
        db = self.client.gitdb
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


if __name__ == '__main__':
    git_username = input('GitHub username: ')
    git_password = input('GitHub password: ')
    # git_password = getpass.getpass('GitHub password: ')
    token = 'use your token'

    win_unicode_console.enable()
    # the mongodb user name and a random password for our cluster
    ds = DataStoring(git_username, git_password, token, 'your cluster username', 'your cluster random password')
    # begin at: 115891102
    print(ds.insert_repositories(115891102, 1).count())
