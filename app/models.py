from app import db, app, bcrypt
import jwt
from sqlalchemy import PrimaryKeyConstraint
import json
# from db import PrimaryKeyConstraint

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
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=60), #TODO: read this value from config
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
            # Expiration time is automatically verified in jwt.decode() and raises jwt.ExpiredSignatureError if the expiration time is in the past
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            print('Signature expired. Please log in again.')
            raise Exception('Signature expired. Please log in again.')
        except jwt.InvalidTokenError:
            print("Invalid token. Please log in again.")
            raise 'Invalid token. Please log in again.'

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Debt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payer = db.Column(db.Integer, nullable=False)
    receiver = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Numeric, nullable=False)

    def __repr__(self):
        return f'Debt: {self.payer} owes {self.receiver} ${self.amount}'

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, nullable=False)      # e.g. spicy_tree_house_group

class Group_Expense(db.Model):
    expense_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, nullable=False)
    expense_name = db.Column(db.String(120), index=True)    # e.g. grocery expenses

    @property
    def serialize(self):
       return {
           'expense_id': self.expense_id,
           'group_id':  self.group_id,
           'expense_name'  : self.expense_name
       }



class Member(db.Model):
    def __init__(self, user_id, group_id, pending):
        self.user_id = user_id
        self.group_id = group_id
        self.pending = pending
    # e.g. Ali is part of spicy_tree_house_group
    user_id = db.Column(db.Integer, primary_key = True)   # FK to user
    group_id = db.Column(db.Integer, primary_key = True)    # FK to Group         
    pending = db.Column(db.Boolean, nullable=False)     # other members (or an admin member need to approve the joining)
    # __table_args__ = (
    #     PrimaryKeyConstraint('user_id', 'group_id'),
    # )

class Member_Expense_Share(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    group_expense_id = db.Column(db.Integer, primary_key = True)
    share = db.Column(db.Numeric, nullable=False)
    # pending = db.Column(db.Boolean, nullable=False)       TODO how to do migration in flask-sql-alchemy
    # __table_args__ = (
    #     PrimaryKeyConstraint('user_id', 'group_expense_id'),
    # )

