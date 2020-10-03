from datetime import datetime
import hashlib
import base64
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
        
        if "alias" not in kwargs:
            self.alias = self.shorten_url(kwargs["long_url"])

    def shorten_url(long_url):
        hashed = hashlib.md5(long_url.encode()).digest()
        b64 = base64.b64encode(hashed, altchars='~_'.encode())
        short_url = b64[:8].decode('ascii')

        return short_url 
