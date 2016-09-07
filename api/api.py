import sys
sys.path.append('/home/felipe/Projs/python/classydoc')
import mymodel

from sqlalchemy import create_engine
from functools import wraps
from flask import request, Response, Flask
from mymodel.user import User
from sqlalchemy.orm import sessionmaker

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
        if not auth or not User.check_auth(auth.username, auth.password):
            return authenticate()
        return f(auth.username)
    return decorated

@app.route('/user/login', methods=['POST'])
@requires_auth
def user_login(username):

    token = get_token();
    return Response("okay", 200, {"token": token})

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

#TODO: give a better token
def get_token():
    return "thisisasecuretoken"
