from flask import Flask
from flask_restful import Resource, Api
from webargs import fields
from webargs.flaskparser import use_args
import markdown 
import os 

app = Flask(__name__)
api = Api(app)

@app.route("/")
def index():
    """Present API Documentation"""

    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as readme:
        content = readme.read()
        return markdown.markdown(content)

class Shortened_URL(Resource):
    def get(self, alias):
        return {'message': 'success', 'alias': alias}, 200

    @use_args({'alias': fields.Str(required=True)}, location='query')
    def post(self, args):
        return {'message': 'success', 'alias': args['alias']}, 201

api.add_resource(Shortened_URL, '/u', '/u/<alias>')