import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

HOST = os.environ.get('HOST', default='0.0.0.0')
DEBUG = bool(int(os.environ.get('DEBUG', default='1')))

app.config["SECRET_KEY"] = "please-remember-to-change-me"
app.config["JWT_SECRET_KEY"] = "please-remember-to-change-me"
app.config["JWT_ALGORITHM"] = "HS256"
app.config['JWT_IDENTITY_CLAIM'] = 'sub'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
jwt = JWTManager(app)

# S3 bucket configuration
S3_BUCKET = "vitor-vendrami-verzel"
app.config['S3_BUCKET'] = S3_BUCKET
app.config['S3_KEY'] = "AKIA2KIYBMFN7XC6AGB5"
app.config['S3_SECRET'] = "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"
app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

#importing routes
from routes.AuthRoute import *
from routes.UserRoute import *
from routes.CarsRoute import *

#Uncomment this section to create the tables
# from models.UserModel import Users
# from models.CarsModel import Cars
# from db import *

if __name__ == '__main__':
    app.run(host=HOST, debug=DEBUG)

