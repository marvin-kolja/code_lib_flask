# app/dash/__init__.py

from flask import Blueprint

dash = Blueprint(
    'dash',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from . import views