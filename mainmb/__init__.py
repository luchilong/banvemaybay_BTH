from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager

mainmb = Flask(__name__)


mainmb.secret_key = "^%@&^@*&!@67532623^@%^%@!"
mainmb.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/bvmbdb?charset=utf8mb4'
mainmb.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=mainmb)
# admin = Admin(app=app, template_mode="bootstrap4")
