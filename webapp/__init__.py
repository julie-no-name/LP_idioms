from flask import Flask, render_template
from webapp.model import db, Idioms


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        page_title = "Learn Idioms"
        idioms_list = Idioms.query.all()
        print(idioms_list)
        return render_template('index.html', page_title=page_title, idioms_list=idioms_list)
    return app

app = create_app()
app.run('127.0.0.1',8080)