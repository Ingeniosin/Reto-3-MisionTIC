from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField
from wtforms.fields.simple import TextField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError

class IFlight(FlaskForm):
    origen = SelectField(u'Origen')
    destino = SelectField(u'Destino')
    fechaSalida = DateField('Fecha salida', format='%d/%m/%Y')
    tiempoVuelo = TextField()
    piloto = SelectField(u'Piloto')
    avion = SelectField(u'Avion')


    def __init__(self,listaLugares, listaPiloto, listaAvion, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.origen.choices= listaLugares
        self.destino.choices= listaLugares
        self.piloto.choices= listaPiloto
        self.avion.choices= listaAvion
