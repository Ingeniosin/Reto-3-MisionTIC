from logging import log
from flask_wtf import FlaskForm
from peewee import IntegerField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextField, DateField, IntegerField
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.widgets.html5 import NumberInput
from datetime import datetime


def getApp():
    import app
    return app.App.__instance__

class RegistroForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(message="El nombre es invalido."), Length(1, 64, message="El nombre es invalido."), Regexp('^[A-Za-z ][A-Za-z0-9_. ]*$', message="El nombre es invalido.")])
    email = StringField('Correo', validators=[DataRequired(message="El email es invalido."), Length(1, 64, message="El email es invalido."), Email(message="El email es invalido.")])
    password = PasswordField('Contraseña', validators=[DataRequired(message="La contraseña es invalida."), EqualTo('confirmpassword', message='Las contraseñas no coinciden.')])
    confirmpassword = PasswordField(validators=[DataRequired(message="Debes confirmar tu contraseña.")])

    def validate_email(self, field):
        from src.model.Entity import Usuario
        if Usuario.select().where(Usuario.correo == field.data).exists():
            raise ValidationError("Este usuario ya esta registrado")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message="El email es invalido."), Length(1, 64, message="El email es invalido."), Email(message="El email es invalido.")])
    password = PasswordField('Password', validators=[DataRequired(message="La contraseña es invalida.")])

    def validate_email(self, field):
        from src.model.Entity import Usuario
        searchUser = Usuario.get_or_none(Usuario.correo == field.data)
        if searchUser == None:
            raise ValidationError("Este usuario no existe.")
        self.user = searchUser

    def validate_password(self, field):
        if self.user is None:
            raise ValidationError("Usuario invalido.")
        passwordValid = self.user.contrasena == field.data
        if not passwordValid:
            raise ValidationError("Las credenciales son invalidas.")


class GestionCrearVuelo(FlaskForm):
    id = HiddenField()
    origen = SelectField(u'Origen', choices= getApp().lugaresTouple)
    destino = SelectField(u'Destino', choices= getApp().lugaresTouple)
    fechaSalida = DateTimeLocalField('Fecha salida', format='%Y-%m-%dT%H:%M', default = datetime.now().strftime('%Y-%m-%dT%H:%M'))
    tiempoVuelo = IntegerField("Tiempo de vuelo (Minutos)", widget=NumberInput(), default = 45)
    piloto = SelectField(u'Piloto', choices=getApp().pilotosTouple)
    avion = SelectField(u'Avion', choices=getApp().avionesTouple)
    capacidad = IntegerField('Capacidad maxima pasajeros', widget=NumberInput(), default = 120)

    def fill(self, vuelo):
        if vuelo is None:
            return self
        self.id.data = vuelo.id
        self.origen.data = vuelo.origen
        self.destino.data = vuelo.destino
        self.fechaSalida.data = vuelo.fecha_salida.strftime('%Y-%m-%dT%H:%M')
        self.tiempoVuelo.data = int((vuelo.fecha_llegada-vuelo.fecha_salida).total_seconds() / 60)
        self.piloto.data = vuelo.piloto
        self.capacidad.data  = vuelo.capacidad
        self.avion.data  = vuelo.avion
        return self