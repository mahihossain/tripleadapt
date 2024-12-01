from flask import Flask
import sys
import os

path = os.path.abspath(__file__)
path = os.path.abspath(os.path.join(path, os.pardir))
path = os.path.abspath(os.path.join(path, os.pardir))
path = os.path.abspath(os.path.join(path, os.pardir))
path = os.path.abspath(os.path.join(path, os.pardir))
sys.path.append(path)

import Backend.config as conf


def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = conf.url_db
    return app


app = create_app()

from Backend.server.app import routes