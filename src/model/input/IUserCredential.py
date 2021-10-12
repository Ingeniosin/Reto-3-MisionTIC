from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField 
from wtforms.validators import DataRequired, Length, Email, ValidationError

class IUserCredential(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message="El email es invalido."), Length(1, 64, message="El email es invalido."), Email(message="El email es invalido.")])
    password = PasswordField('Password', validators=[DataRequired(message="La contraseña es invalida.")])

    def validate_email(self, field):
        from src.model.entity.User import User
        searchUser = User.get_or_none(User.email == field.data)
        if searchUser == None:
            raise ValidationError("Este usuario no existe.")
        self.user = searchUser

    def validate_password(self, field):
        if self.user is None:
            raise ValidationError("Usuario invalido.")
        passwordValid = self.user.password == field.data
        if not passwordValid:
            raise ValidationError("Las credenciales son invalidas.")
