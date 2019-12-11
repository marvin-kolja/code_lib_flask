# app/signup/__init__.py

from flask import Blueprint

signup = Blueprint(
    'signup',
    __name__
)

from . import views