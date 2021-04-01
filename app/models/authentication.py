from .. import db

class Authentication(db.Model):
    __tablename__ = 'authentication'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    createTime = db.Column(db.Integer)