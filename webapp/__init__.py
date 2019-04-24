from flask import Flask, render_template, request, flash, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, current_user
from webapp.model import db, Idioms, User
from webapp.forms import LoginForm, RegistrationForm
from flask_migrate import Migrate
import random
from sqlalchemy.sql import func



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def index():
        page_title = "Learn Idioms"
        idioms_list = Idioms.query.all()
        return render_template('index.html', page_title=page_title, idioms_list=idioms_list)


    @app.route('/search')
    def search():
        page_title = "Search Idioms"
        idioms_list = Idioms.query
        if request.args.get('q'):
            search_term = f"{request.args.get('q')}%"
            idioms_list = idioms_list.filter(Idioms.name_of_idiom.like(search_term))
        return render_template('search.html', page_title=page_title, idioms_list=idioms_list.all())


    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
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

    

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы вошли на сайт')
                return redirect(url_for('index'))
        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))


    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))


    @app.route('/register')
    def register():
        if current_user.is_authenticated:
            flash('Вы уже зарегистрировались и вошли на сайт')
            return redirect(url_for('index'))
        form = RegistrationForm()
        title = "Регистрация"
        return render_template('registration.html', page_title=title, form=form)


    @app.route('/process-reg', methods=['POST'])
    def process_reg():
        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = User(username=form.username.data, email=form.email.data, role='user')
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Вы успешно зарегистрировались!')
            return redirect(url_for('login'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Ошибка в поле "{}": - {}'.format(
                        getattr(form, field).label.text,
                        error
                    ))
            return redirect(url_for('register'))
        flash('Пожалуйста, исправьте ошибки в форме')
        return redirect(url_for('register'))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run('127.0.0.1', 8087, debug=True)
