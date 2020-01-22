# app/id_handler/__init__.py

from flask import Blueprint

id_handler = Blueprint(
    'id_handler',
    __name__
)

from . import views