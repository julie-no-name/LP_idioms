from flask import Flask, render_template, request, flash
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

        if request.args.get('answer') and request.args.get('question'):
            if request.args.get('answer') == request.args.get('question'):
                flash('Your previous answer was right!')
            else:
                flash('Your previous answer was wrong!')
        
        page_title = "Practice"
        variants = []
        for idiom in Idioms.query.order_by(func.random()).limit(4).all():
            variants.append(idiom)
        question_idiom = variants[0]
        
 
        return render_template('practice.html', page_title=page_title,
            question_idiom=question_idiom, variants=variants)

    

    return app


if __name__ == "__main__":
    app = create_app()
    app.run('127.0.0.1', 8087, debug=True)