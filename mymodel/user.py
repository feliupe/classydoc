#TODO: decouple this
import sys
sys.path.append('/home/felipe/Projs/python/classydoc')
import api

from mymodel import Base,db
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    exp = db.Column(db.DateTime())
    token = db.Column(db.String(50))

    @staticmethod
    def check_authentication(username, password):
        """This function is called to check if a username /
        password combination is valid.
        """
        user = api.session.query(User).filter(User.username == username and User.password_hash == password).first()
        return True if user else False

    @staticmethod
    def check_authorization(token):
        """Check if the authorization token is valid"""
        s = Serializer(api.app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token

        user = api.session.query(User).filter(User.id == data['id']).first()

        return user
        
    #TODO: give a better token
    def get_token(self, expiration = 600):
        #Decouple
        s = Serializer(api.app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })
