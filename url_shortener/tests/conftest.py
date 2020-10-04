import pytest
from flask import Flask
from src.routes import short

@pytest.fixture(scope='session', autouse=True)
def app():
    app = Flask(__name__)        
    app.register_blueprint(short)
    return app 

@pytest.fixture(scope='function')
def db():
    return []