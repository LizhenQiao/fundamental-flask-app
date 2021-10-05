from flask import Flask


webapp = Flask(__name__)

from app import admin
from app import login
from app import main