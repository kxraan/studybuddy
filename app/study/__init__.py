# app/study/__init__.py
from flask import Blueprint

study = Blueprint('study', __name__, url_prefix='/study')

from app.study import routes  
