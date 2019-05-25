from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

from app.api import bp as api_bp
CORS(api_bp, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(api_bp, url_prefix='/api')

from app import routes, models