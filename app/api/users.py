from app.api import bp
from flask import request, make_response, jsonify
from app.models import User
from app import bcrypt, db

@bp.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    return "hi " + str(id)

@bp.route('/user/register', methods=['POST'])
def register():
    print("\n****HERE!\n")
    # get the post data
    post_data = request.get_json()
    # check if user already exists
    user = User.query.filter_by(email=post_data.get('email')).first()
    if not user:
        try:
            user = User(
                email=post_data.get('email'),
                password=post_data.get('password')
            )

            print(user.id)

            # insert the user
            db.session.add(user)
            db.session.commit()

            print(user.id)

            # generate the auth token
            auth_token = user.encode_auth_token(user.id)
            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred while registering user. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(responseObject)), 202

    
@bp.route('/user/login', methods=['POST'])
def login():
    # get the post data
    post_data = request.get_json()
    try:
        # fetch the user data
        user: User = User.query.filter_by(
            email=post_data.get('email')
        ).first()
        if user and user.check_password(post_data.get('password')):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return make_response(jsonify(responseObject)), 404
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(responseObject)), 500

