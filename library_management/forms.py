from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[DataRequired()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])

class BookForm(FlaskForm):
    title = StringField('Tên sách', validators=[DataRequired(), Length(max=150)])
    author = StringField('Tác giả', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Mô tả')

class SignupForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[DataRequired(), Length(max=80)])
    password = PasswordField('Nhập mật khẩu', validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField('Nhập lại mật khẩu', validators=[DataRequired(), EqualTo('password', message='Mật khẩu không khớp')])