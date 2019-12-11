# app/reader/__init__.py

from flask import Blueprint

scanner = Blueprint(
    'scanner',
    __name__
)

from . import views