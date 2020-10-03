from flask import Blueprint
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs
import markdown 
import os  
from datetime import datetime

from .extensions import db
from .models import Link, shorten_url


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
@use_kwargs({'url': fields.Str(required=True), 'custom_alias': fields.Str(required=False)}, location='query')
def add_link(**kwargs):
    start_time = datetime.now()

    if 'custom_alias' in kwargs:
        alias = kwargs['custom_alias']
    else:
        alias = shorten_url(kwargs['url'])
    
    new_short_url = Link(long_url=kwargs['url'], alias=alias)

    db.session.add(new_short_url)
    db.session.commit()
    
    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds() * 1000

    return {
        'message': 'Short URL created', 
        'url': new_short_url.long_url, 
        'custom_alias': new_short_url.alias,
        'time_taken': f'{execution_time}ms'
        }, 201