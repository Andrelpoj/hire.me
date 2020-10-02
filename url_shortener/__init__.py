from flask import Flask
from flask_restful import Resource, Api
from webargs import fields
from webargs.flaskparser import use_args
import markdown 
import os  

from .models import Short_URLs, db
from . import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db.init_app(app)
db.create_all()
        
api = Api(app)


@app.route("/")
def index():
    """Present API Documentation"""

    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as readme:
        content = readme.read()
        return markdown.markdown(content)


class Short_URL(Resource):
    def get(self, alias):
        short_url = Short_URLs.query.get(alias)

        return { 
            'alias': short_url.alias,
            'long_url': short_url.url
            }, 200

    @use_args({
        'url': fields.Str(required=True),
        'custom_alias': fields.Str(required=True)
        }, location='query')
    def post(self, args):
        
        new_short_url = Short_URLs(alias=args['custom_alias'], url=args['url'])
        db.session.add(new_short_url)
        db.session.commit()
        
        return {
            'message': 'Added', 
            'url': args['url'], 
            'custom_alias': args['custom_alias']
            }, 201


api.add_resource(Short_URL, '/u', '/u/<alias>')