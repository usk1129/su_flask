from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import yaml 

config_file = 'config.yaml'
with open(config_file,'r') as ymlfile:
    cfg = yaml.load(ymlfile)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = cfg['database_path']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes
