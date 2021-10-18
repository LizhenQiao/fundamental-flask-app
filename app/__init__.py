from flask import Flask



webapp = Flask(__name__)
webapp.secret_key = "you-will-never-know-lol"
webapp.jinja_env.auto_reload = True
webapp.config['TEMPLATES_AUTO_RELOAD'] = True
webapp.config['SESSION_TYPE'] = 'filesystem'


from app import admin
from app import main
from app import admin
from app import user
from app import api