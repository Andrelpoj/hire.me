from flask import Flask
from .extensions import db
from .routes import short
from . import config

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()

    db.init_app(app)
    db.create_all()
            
    app.register_blueprint(short)

    return app