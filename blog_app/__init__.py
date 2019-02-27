from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

from flask_login import LoginManager



app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#create a database instance
db = SQLAlchemy(app)

#initialise flask_bcrypt
bcrypt = Bcrypt(app)

#initialize login manager
login_manager = LoginManager(app)
#set the login route
login_manager.login_view = 'login'
#beatify the message using bootstrap
login_manager.login_message_category = 'info' #infomation alert flash message

#import our routes here
from blog_app import routes