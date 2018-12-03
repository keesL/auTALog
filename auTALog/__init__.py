from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
import flask_security 


app = Flask(__name__)
app.config['SECURITY_PASSWORD_SALT'] = 'unused'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# BEGIN FIXME  
# this is somewhat acceptable which developing, but make sure
# to take these settings out of the main source code repo and
# move it to an untracked config file

app.secret_key = b'M\xc8\x07\x02\xc7\xa4Y_\x99\x90\x0c\xf6r\xceY4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://autalog:autalog@localhost/autalog'

# END FIXME

Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import auTALog.views
from auTALog.models import User, Role

# Setup Flask-Security
user_datastore = flask_security.SQLAlchemyUserDatastore(db, User, Role)
security = flask_security.Security(app, user_datastore)

def setupDB():
	adminRole = Role(name="admin", description="Admin role")
	taRole = Role(name="ta", description="Teaching assistant")
	db.session.add(adminRole)
	db.session.add(taRole)
	db.session.commit()