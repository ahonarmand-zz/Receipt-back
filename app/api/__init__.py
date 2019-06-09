from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')

from app.api import user, errors, tokens, group, member, group_expense # TODO: can I put * here?