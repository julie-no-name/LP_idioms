from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Idioms(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name_of_idiom = db.Column(db.Text, unique = True)
    translation = db.Column(db.Text, unique = True)
    definition = db.Column(db.Text, unique = True)

    def __repr__(self):
        return f'<Idioms {self.name_of_idiom} {self.translation} {self.definition}>'
