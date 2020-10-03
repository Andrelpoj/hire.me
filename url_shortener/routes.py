from flask import Blueprint
from webargs import fields
from webargs.flaskparser import use_args
import markdown 
import os  
from datetime import datetime


from .extensions import db
from .models import Link

short = Blueprint('short', __name__)

@short.route("/")
def index():
    """Present API Documentation"""

    with open(os.path.abspath("README.md"), 'r') as readme:
        content = readme.read()
        return markdown.markdown(content)


@short.route('/<alias>',methods=['GET'])
def get_link(alias):
    link = Link.query.filter_by(alias=alias).first_or_404()

    return { 
        'alias': link.alias,
        'long_url': link.long_url,
        }, 200

@short.route('/u', methods=['POST'])
@use_args({'url': fields.Str(required=True), 'custom_alias': fields.Str(required=True)}, location='query')
def add_link(args):
    start_time = datetime.now()

    new_short_url = Link(alias=args['custom_alias'], long_url=args['url'])
    db.session.add(new_short_url)
    db.session.commit()
    
    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds() * 1000

    return {
        'message': 'Short URL created', 
        'url': args['url'], 
        'custom_alias': args['custom_alias'],
        'time_taken': f'{execution_time}ms'
        }, 201