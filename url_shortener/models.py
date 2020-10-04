from datetime import datetime
import hashlib
import base64
import random
import string

from .extensions import db


class Link(db.Model):
    __tablename__ = 'link'
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(512))
    alias = db.Column(db.String(8), unique=True)
    visits = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        
        if "alias" in kwargs:
            link = Link.query.filter_by(alias=kwargs["alias"]).first() 
            if link:
                raise AliasAlreadyExists(kwargs["alias"])
        else:
            self.alias = self.shorten_url(kwargs["long_url"])

def shorten_url(long_url):
    hashed = hashlib.md5(long_url.encode()).digest()
    b64 = base64.b64encode(hashed, altchars='~_'.encode())
    short_url = b64[:8].decode('ascii')

    #Deals with collisions
    if alias_exists(short_url):            
        random_sufix = ''.join(random.choices(string.ascii_letters, k=3))
        return shorten_url(long_url + random_sufix)

    return short_url 

def alias_exists(alias):
    if Link.query.filter_by(alias=alias).first():
        return True 
    return False

class AliasAlreadyExists(Exception):
    def __init__(self, alias):
        self.alias = alias
