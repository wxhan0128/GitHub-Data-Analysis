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

    # configure the MongoDB connections
    MONGO_HOST = 'mongodb://cluster0-shard-00-00-i6gcp.mongodb.net/?ssl=true'
    MONGO_USERNAME = 'Campione'
    MONGO_PASSWORD = 'veTRxJL29lpKWwPn'
    MONGO_PORT = 27017
    MONGO_AUTH_SOURCE = 'admin'
    MONGO_REPLICA_SET = 'Cluster0-shard-0'
    MONGO_READ_PREFERENCE = 'PRIMARY'
    MONGO_DBNAME = 'gitdbPro'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
