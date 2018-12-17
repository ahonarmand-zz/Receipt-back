from flask import jsonify, make_response, request
from app.models import User
import functools

def login_required(func):

    @functools.wraps(func)
    def wrapper_login_required(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            return make_response(jsonify({"status": 'fail', "message": 'missing credentials'}))
        
        try:
            user_id = User.decode_auth_token(auth_token)

            user = User.query.filter_by(id=user_id).first()
            if user:
                return func(user_id, *args, **kwargs)
        
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': repr(e)
            }
            return make_response(jsonify(responseObject)), 401
    return wrapper_login_required