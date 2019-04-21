from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from webapp.model import User

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class":"form-control", "placeholder":""})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"input type":"password", "class":"form-control", "id":"exampleInputPassword1", "placeholder":""})
    submit = SubmitField('Войти', render_kw={"type":"submit", "class":"btn btn-primary"})

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')], render_kw={"class": "form-control"})
    submit = SubmitField('Зарегистрироваться', render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        users_count = User.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с таким именем уже зарегистрирован')

    def validate_email(self, email):
        users_count = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с такой электронной почтой уже зарегистрирован')