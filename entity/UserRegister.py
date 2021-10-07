from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

class UserRegister(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(message="El nombre es invalido."), Length(1, 64, message="El nombre es invalido."), Regexp('^[A-Za-z ][A-Za-z0-9_. ]*$', message="El nombre es invalido.")])
    email = StringField('Correo', validators=[DataRequired(message="El email es invalido."), Length(1, 64, message="El email es invalido."), Email(message="El email es invalido.")])
    password = PasswordField('Contraseña', validators=[DataRequired(message="La contraseña es invalida."), EqualTo('confirmpassword', message='Las contraseñas no coinciden.')])
    confirmpassword = PasswordField(validators=[DataRequired(message="Debes confirmar tu contraseña.")])