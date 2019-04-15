from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search = StringField('Текст поиска', validators=[DataRequired()], render_kw={"class": "form-control mr-sm-2", "type": "search", "placeholder": "Search", "aria-label": "Search"})
    submit = SubmitField('Искать', render_kw={"class":"btn btn-outline-success my-2 my-sm-0", "type":"submit"})

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class":"form-control", "placeholder":""})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"input type":"password", "class":"form-control", "id":"exampleInputPassword1", "placeholder":""})
    submit = SubmitField('Отправить', render_kw={"type":"submit", "class":"btn btn-primary"})