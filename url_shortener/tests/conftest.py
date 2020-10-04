import pytest
from flask import Flask
from url_shortener.routes import short

@pytest.fixture(scope='session', autouse=True)
def app():
    app = Flask(__name__)        
    app.register_blueprint(short)
    return app 