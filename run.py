import os
from flask import Flask
from detect_api.api import api
from detect_api.api.config import config


config_name = os.environ.get('CONFIG', 'local')
app = Flask(__name__)
app.config.from_object(config[config_name])
app.register_blueprint(api)
