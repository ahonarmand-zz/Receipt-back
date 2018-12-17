from app import db, app, bcrypt
import jwt

import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    profile_pic_path = db.Column(db.String(200), unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, password, name = None, profile_pic_path = None):
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password)    #complexity can e increased by setting log_rounds
        self.name = name
        self.profile_pic_path = profile_pic_path

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
        
    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=10),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise Exception('Signature expired. Please log in again.')
        except jwt.InvalidTokenError:
            raise 'Invalid token. Please log in again.'

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Debt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payer = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Numeric, nullable=False)

    def __repr__(self):
        return f'Debt of {self.amount} from {self.payer} to {self.received}'