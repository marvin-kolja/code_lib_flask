# app/dash/__init__.py

from flask import Blueprint

dash = Blueprint(
    'dash',
    __name__
)

from . import views