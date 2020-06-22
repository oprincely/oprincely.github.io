from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager



app = Flask(__name__)

app.config.from_object(Config) 

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)

login = LoginManager(app)
login.login_view = 'login'

from numerology import main, models
#app.config["DEBUG"] = True

#app.config['dbconfig'] = { 'host': 'localhost','user': 'wecorgng','password': 'spyWIZARD','database': 'wecorgng_user', }
#app.secret_key = "SOMETHINGWithMeIn#RoomsRANDOM"
    
'''
import vsearch
app.register_blueprint(vsearch.bp)

from account import acct as acct_blueprint
app.register_blueprint(acct_blueprint)

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from sqldb import sqldb as sqldb_blueprint
app.register_blueprint(sqldb_blueprint)
'''
#from numerology import main as main_blueprint
#app.register_blueprint(main_blueprint)
'''
import newuser
app.register_blueprint(newuser.bp)

import blog
app.register_blueprint(blog.bp)

import transit
app.register_blueprint(transit.bp)
'''