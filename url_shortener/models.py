import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class Short_URLs(db.Model):
    __tablename__ = 'shorturls'
    alias = db.Column(db.String(16), primary_key=True)
    url = db.Column(db.String(512))