import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get(
        'FLASKBE_SECRET_KEY',
        '51f52814-0071-11e6-a247-000ec6c2372c'
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'FLASKBE_SQLALCHEMY_DATABASE_URI',
        'sqlite:///' + os.path.join(basedir, 'flaskbe.db')
    )
    SQLALCHEMY_MIGRATE_REPO = os.environ.get(
        'FLASKBE_SQLALCHEMY_MIGRATE_REPO',
        os.path.join(basedir, 'db_repository')
    )


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}