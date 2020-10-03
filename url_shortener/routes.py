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

    with open(os.path.abspath("README.md"), 'r') as readme:
        content = readme.read()
        return markdown.markdown(content)


@short.route('/<alias>',methods=['GET'])
def get_link(alias):
    link = Link.query.filter_by(alias=alias).first()

    if not link:
        return {
            'alias': alias,
            'err_code': '002',
            'description': 'Shortened URL not found'
        }, 404

    #Updates visits
    link.visits += 1
    db.session.commit()

    #Guarantees redirect to a Full URL
    url = link.long_url
    if url.find("http://") != 0 and url.find("https://") != 0:
        url = "http://" + url
         
    return redirect(url, code=302)

@short.route('/addlink', methods=['POST'])
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
        'alias': new_short_url.alias,
        'url': new_short_url.long_url, 
        'time_taken': f'{execution_time}ms'
    }, 201

@short.route('/top', methods=['GET'])
def get_top_links():
    links = Link.query.order_by(Link.visits.desc()).limit(10)

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