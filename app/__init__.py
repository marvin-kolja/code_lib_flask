from flask import Flask
from .admin import admin
from .login import login
from .signup import signup
from .dash import dash
from .home import home
from .id_handler import id_handler

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

app.register_blueprint(admin)
app.register_blueprint(login)
app.register_blueprint(signup)
app.register_blueprint(dash)
app.register_blueprint(home)
app.register_blueprint(id_handler)
