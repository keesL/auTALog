from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_security.utils import hash_password
from auTALog import config
import flask_security 


app = Flask(__name__)
app.config['SECURITY_PASSWORD_SALT'] = 'unused'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BOOTSTRAP_USE_MINIFIED'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = config.config['db_uri']
app.secret_key=config.config['secret_key']

Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import auTALog.views
from auTALog.models import User, Role

# Setup Flask-Security
user_datastore = flask_security.SQLAlchemyUserDatastore(db, User, Role)
security = flask_security.Security(app, user_datastore)


def setupDB():
    with app.app_context():
        adminRole = Role(name="admin", description="Admin role")
        tutorRole = Role(name="tutor", description="Tutor")
        graderRole = Role(name="grader", description="Grader")

        adminUser = User(email="leune@adelphi.edu", password=hash_password('hello'))

        db.session.add(adminUser)
        db.session.add(adminRole)
        db.session.add(tutorRole)
        db.session.add(graderRole)
        db.session.commit()

        ins = roles_users.insert().values(user_id=adminUser.id, role_id=adminRole.id)
        db.session.execute(ins)
