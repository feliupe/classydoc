class Default:
    DEBUG = False
    TESTING = False
    #In memory
    DATABASE_URI = 'sqlite://'

class Test(Default):
    DEBUG = True
    TESTING = True

class Production(Default):
    DATABASE_URI = "sqlite:////home/felipe/Projs/python/classydoc/sqlalchemy_example.db"
