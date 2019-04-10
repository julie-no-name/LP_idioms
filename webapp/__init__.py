from flask import Flask, render_template, request
from webapp.model import db, Idioms
from webapp.forms import SearchForm


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/', methods = ['GET', 'POST'])
    def index():
        form = SearchForm()
        page_title = "Learn Idioms"
        if form.validate_on_submit():
            search_term = f'{form.search.data}%'
            idioms_list = Idioms.query.filter(Idioms.name_of_idiom.like(search_term)).all()
            return render_template('index.html', page_title=page_title, idioms_list=idioms_list, form=form)
        idioms_list = Idioms.query.all()
        return render_template('index.html', page_title=page_title, idioms_list=idioms_list, form=form)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run('127.0.0.1', 8099, debug=True)