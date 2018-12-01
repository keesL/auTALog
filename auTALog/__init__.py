from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
import flask_security 


app = Flask(__name__)
app.secret_key = b'M\xc8\x07\x02\xc7\xa4Y_\x99\x90\x0c\xf6r\xceY4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://autalog:autalog@localhost/autalog'
app.config['SECURITY_PASSWORD_SALT'] = 'unused'

Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import auTALog.views
from auTALog.models import User, Role

# Setup Flask-Security
user_datastore = flask_security.SQLAlchemyUserDatastore(db, User, Role)
security = flask_security.Security(app, user_datastore)

