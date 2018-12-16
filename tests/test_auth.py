import time
import json
import unittest

from app import db

from tests.base import BaseTestCase

def register_user(self, email, password):
        print("\n ****** in register_user \n")
        print(self.client)
        print(type(self.client))
        return self.client.post('api/user/register', data=json.dumps(dict(email=email,password=password)), content_type='application/json')

def login_user(self, email, password):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json',
    )

class TestAuthBlueprint(BaseTestCase):
    def test_registration(self):
        """ Test for user registration """
        with self.client:
            # response = register_user(self, 'joe@gmail.com', '123456')
            response = self.client.post('api/user/register', data=json.dumps(dict(email='joe@gmail.com',password='123456')), content_type='application/json')
            print(response)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_dummy(self):
        with self.client:
            response = self.client.get('api/user/2', content_type='application/json')
            print(response.data)
            print(response.data.decode())
