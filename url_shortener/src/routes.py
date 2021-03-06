from flask import Blueprint, request, redirect
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs
import markdown 
import os  
from datetime import datetime

from .extensions import db
from .models import Link, shorten_url, AliasAlreadyExists


short = Blueprint('short', __name__)

@short.route("/")
def index():
    """Present API Documentation"""

    with open(os.path.abspath("./docs/API_DOC.md"), 'r') as readme:
        content = readme.read()
        return markdown.markdown(content)


@short.route('/<alias>',methods=['GET'])
def get_link(alias):
    """ Retrieve URL Endpoint """

    link = Link.find_by_alias(alias)

    if not link:
        return {
            'alias': alias,
            'err_code': '002',
            'description': 'Shortened URL not found'
        }, 404

    link.increment_visits()
 
    return redirect(link.long_url, code=302)


@short.route('/addlink', methods=['POST'])
@use_kwargs({'url': fields.Url(required=True), 'custom_alias': fields.Str(required=False)}, location='query')
def add_link(**kwargs):
    """ Shorten URL Endpoint """
    
    start_time = datetime.now()

    if 'custom_alias' in kwargs:
        alias = kwargs['custom_alias']
    else:
        alias = shorten_url(kwargs['url'])
    
    new_short_url = Link(long_url=kwargs['url'], alias=alias)
    new_short_url.save_to_database()

    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds() * 1000

    return {
        'message': 'Short URL created', 
        'alias': new_short_url.alias,
        'url': new_short_url.long_url, 
        'time_taken': f'{execution_time}ms'
    }, 201


@short.route('/top', methods=['GET'])
def get_top_links():
    """ Top URLs Endpoint"""
    
    links = Link.top_most_visited()

    result = {}
    for link in links:
        result[link.alias] = link.visits

    return result, 200

@short.errorhandler(AliasAlreadyExists)
def handle_alias_already_exists(e):
    return {
            'alias': e.alias,
            'err_code': '001',
            'description': 'Custom Alias already exists'
        }, 400