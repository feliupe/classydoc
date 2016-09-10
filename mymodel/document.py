#TODO: decouple this
import sys
sys.path.append('/home/felipe/Projs/python/classydoc')
import api

from mymodel import Base,db
import os

class Document(Base):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), index = True)
    user_id = db.Column(db.Integer)
    category = db.Column(db.String(32), index = True)

    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self.documents_path = os.path.join(api.app.config['APPLICATION_ROOT'], 'documents')

    def save(self, text):
        os.makedirs(self._user_dir(), exist_ok=True)

        with open(self._file_path(self.name), 'w', encoding="utf-8") as stream:
            stream.write(text)

        api.session.add(self)
        api.session.commit()

    def text(self):
        with open(self._file_path(self.name), encoding="utf-8") as stream:
            return stream.read()

    def _user_dir(self):
        return os.path.join(self.documents_path, str(self.user_id))

    def _file_path(self, filename):
        return os.path.join(self._user_dir(), filename)
