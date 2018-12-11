import unittest

from app import app
from flask_testing import TestCase

class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.Config')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'you-will-never-guess')

