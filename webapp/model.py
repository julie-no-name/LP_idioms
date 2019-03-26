from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Idioms(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name_of_theme = db.Column(db.String, unique = True, nullable=False)
    name_of_idiom = db.Column(db.String, unique = True, nullable=False)
    translation = db.Column(db.String, nullable=False)
    definition = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Idioms {self.name_of_idiom} {self.translation} {self.definition}>'
