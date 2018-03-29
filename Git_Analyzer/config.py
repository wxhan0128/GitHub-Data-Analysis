from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class Config(object):

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True


class DevelopmentConfig(Config):
    DEBUG = True

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


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
