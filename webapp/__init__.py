from flask import Flask, render_template, request, flash, redirect,url_for
from flask_login import LoginManager, login_user, logout_user
from webapp.model import db, Idioms, User
from webapp.forms import SearchForm, LoginForm


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

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


    return app


if __name__ == "__main__":
    app = create_app()
    app.run('127.0.0.1', 8087, debug=True)