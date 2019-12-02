# app/signup/__init__.py

from flask import Blueprint

signup = Blueprint(
    'signup',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from . import views