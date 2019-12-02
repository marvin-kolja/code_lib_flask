# app/reader/__init__.py

from flask import Blueprint

scanner = Blueprint(
    'scanner',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from . import views