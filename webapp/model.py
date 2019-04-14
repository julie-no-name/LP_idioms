from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Idioms(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name_of_theme = db.Column(db.String, nullable=False,index=True)
    name_of_idiom = db.Column(db.String, unique = True, nullable=False, index=True)
    translation = db.Column(db.String, nullable=False, index=True)
    definition = db.Column(db.Text, nullable=False, index=True)

    def __repr__(self):
        return f'<Idioms {self.name_of_idiom} {self.translation} {self.definition}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

