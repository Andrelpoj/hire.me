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
    alias = db.Column(db.String(12), unique=True)
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
    
    def increment_visits(self):
        self.visits += 1
        db.session.commit()
    
    def save_to_database(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod 
    def find_by_alias(alias):
        return Link.query.filter_by(alias=alias).first()

    # @staticmethod
    # def alias_exists(alias):
    #     return bool(find_by_alias)

def shorten_url(long_url):
    """ 
        Returns a unique alias for a long_url.

        1. Receives a string
        2. Applies hashing algorithm - MD5
        3. Applies encoding of base64
        4. Returns an slice of 8 characters
    """
    hashed = hashlib.md5(long_url.encode()).digest()
    b64 = base64.b64encode(hashed, altchars='~_'.encode())
    alias = b64[:8].decode('ascii')

    #Deals with collisions
    if Link.find_by_alias(alias):            
        random_sufix = ''.join(random.choices(string.ascii_letters, k=3))
        return shorten_url(long_url + random_sufix)

    return alias 

class AliasAlreadyExists(Exception):
    def __init__(self, alias):
        self.alias = alias
