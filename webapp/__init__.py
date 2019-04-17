from flask import Flask, render_template, request
from webapp.model import db, Idioms
from webapp.forms import SearchForm, LoginForm
import random
from sqlalchemy.sql import func



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/', methods = ['GET', 'POST'])
    def index():
        form = SearchForm()
        page_title = "Learn Idioms"
        idioms_list = Idioms.query
        if request.method == 'POST':
            if form.validate_on_submit():
                search_term = f'{form.search.data}%'
                idioms_list = idioms_list.filter(Idioms.name_of_idiom.like(search_term))
        return render_template('index.html', page_title=page_title, idioms_list=idioms_list.all(), form=form)


    @app.route('/login')
    def login():
        page_title = "Login"
        login_form = LoginForm()
        return render_template('login.html', page_title=page_title, form=login_form)

    @app.route('/practice')
    def practice():
        page_title = "Тренировка"
        variants = []
        random_cell = Idioms.query.order_by(func.random()).first()
        random_idiom = random_cell.name_of_idiom
        variants.append(random_cell.translation)
        variants.append(Idioms.query.order_by(func.random()).first().translation)
        variants.append(Idioms.query.order_by(func.random()).first().translation)
        variants.append(Idioms.query.order_by(func.random()).first().translation)
        random.shuffle(variants)
        idioms_list = Idioms.query
        
 
        return render_template('practice.html', page_title=page_title, idioms_list=idioms_list.all(),
            random_idiom=random_idiom, variants=variants)

    
    @app.route('/answer')
    def answer():
        page_title = "Тренировка"
        variants = []
        random_cell = Idioms.query.order_by(func.random()).first()
        random_idiom = random_cell.name_of_idiom
        variants.append(random_cell.translation)
        variants.append(Idioms.query.order_by(func.random()).first().translation)
        variants.append(Idioms.query.order_by(func.random()).first().translation)
        variants.append(Idioms.query.order_by(func.random()).first().translation)
        random.shuffle(variants)
        idioms_list = Idioms.query
        
 
        return render_template('answer.html', page_title=page_title, idioms_list=idioms_list.all(),
            random_idiom=random_idiom, variants=variants)


    return app


if __name__ == "__main__":
    app = create_app()
    app.run('127.0.0.1', 8087, debug=True)