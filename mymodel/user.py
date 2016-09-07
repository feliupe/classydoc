from mymodel import Base,db

#TODO: decouple this
import sys
sys.path.append('/home/felipe/Projs/python/classydoc')
import api

class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    exp = db.Column(db.String(50))
    token = db.Column(db.String(50))

    @staticmethod
    def check_auth(username, password):
        """This function is called to check if a username /
        password combination is valid.
        """

        user = api.session.query(User).filter(User.username == username and User.password_hash == password).first()

        return True if user else False
