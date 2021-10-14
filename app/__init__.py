from flask import Flask


webapp = Flask(__name__)

from app import admin
from app import main
from app import admin
from app import user
from app import api