from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

class UserCredential(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message="El email es invalido."), Length(1, 64, message="El email es invalido."), Email(message="El email es invalido.")])
    password = PasswordField('Password', validators=[DataRequired(message="La contraseña es invalida.")])
