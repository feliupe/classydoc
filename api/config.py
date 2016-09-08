class Default:
    DEBUG = False
    TESTING = False
    #In memory
    DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'crounching tiger hidden dragon'
    APPLICATION_ROOT = '/home/felipe/Projs/python/classydoc/api'

class Test(Default):
    DEBUG = True
    TESTING = True
    APPLICATION_ROOT = '/home/felipe/Projs/python/classydoc/api/test'

class Production(Default):
    DATABASE_URI = "sqlite:////home/felipe/Projs/python/classydoc/sqlalchemy_example.db"
