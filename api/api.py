import sys
sys.path.append('/home/felipe/Projs/python/classydoc')
import mymodel

from sqlalchemy import create_engine
from functools import wraps
from flask import request, Response, Flask, abort, jsonify
from mymodel.user import User
from mymodel.document import Document
from mymodel.doc_classifier import DocClassifier
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

app = Flask(__name__)

def create_app(config='config.Production'):
    global session, engine

    app.config.from_object(config)

    engine = create_engine(app.config['DATABASE_URI'])
    Session = sessionmaker(bind=engine)
    session = Session()

#Default app
create_app()

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not User.check_authentication(auth.username, auth.password):
            return authenticate()
        return f(auth.username)
    return decorated

def requires_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth:
            token = auth.get('username')
            user = User.check_authorization(token) if token else False
            if user:
                return f(user.id)
        return authenticate()
    return decorated

@app.route('/api/token', methods=['GET'])
@requires_auth
def api_token(username):
    user_query = session.query(User).filter(User.username == username)
    user = user_query.first()

    token = user.get_token()

    params = {"token": token, "exp": datetime.now() + timedelta(minutes=5)}

    if user_query.update(params):
        return Response("okay", 200, {"token": token})
    else:
        return abort(500)

@app.route('/user/register', methods=['POST'])
def user_register():
    form = request.form
    user = session.query(User).filter(User.username == form["user"]).first()

    if user:
        return Response("user already exist", 202)

    user = User(username=form["user"],password_hash=form["password"])
    session.add(user)
    session.commit()

    return Response("okay", 200, {"user": user.username})

documents = [
    {
        'id': 1,
        'category': 'Financial'
    },
    {
        'id': 2,
        'category': 'Supply'
    },
    {
        'id': 3,
        'category': 'Financial'
    },
    {
        'id': 4,
        'category': 'Real_Property'
    }
]

@app.route('/user/documents', methods=['GET'])
@requires_token
def get_document_list(id):
    return jsonify({'documents': documents}), 200

@app.route('/user/send', methods=['POST'])
@requires_token
def send_documents(id):

    dc = DocClassifier()
    dc.load_classifier()

    for f in request.files:
        file = request.files[f]
        doc = Document(name=file.filename, user_id=id)
        text = file.read().decode('utf-8')
        doc.category = dc.category(dc.predict(text=text))
        doc.save(text)
        session.add(doc)

    session.commit()

    return Response('Files stored', 200)
