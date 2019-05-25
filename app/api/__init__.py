from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')

from app.api import users, errors, tokens, group, member # TODO: can I put * here?