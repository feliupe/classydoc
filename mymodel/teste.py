from mymodel import Base,db

class Teste(Base):
    __tablename__ = 'teste'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
