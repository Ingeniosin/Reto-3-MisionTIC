from peewee import BooleanField, ForeignKeyField, Model, CharField, DateTimeField, IntegerField, DoubleField
from flask_login import UserMixin
import datetime

class EntityModel(Model):
    class Meta:
        from app import App
        database = App.__instance__.database.database

class Rol(EntityModel):
    nombre = CharField()

class Usuario(EntityModel, UserMixin):
    nombre = CharField()
    correo = CharField(unique = True, index = True)
    contrasena = CharField()
    es_activo = BooleanField(null = False, default=True)
    fecha_creacion = DateTimeField(default = datetime.datetime.now)
    role = ForeignKeyField(Rol)
 
class Lugar(EntityModel):
    nombre = CharField()

class Avion(EntityModel):
    nombre = CharField()
    capacidad = IntegerField()
    foto = CharField()

class Vuelo(EntityModel):
    codigo = CharField()
    origen = ForeignKeyField(Lugar)
    destino = ForeignKeyField(Lugar)
    estado = CharField()
    capacidad = IntegerField()
    avion = ForeignKeyField(Avion)
    fecha_salida = DateTimeField(default = datetime.datetime.now)
    fecha_llegada = DateTimeField(default = datetime.datetime.now)
    piloto = ForeignKeyField(Usuario)

class UsuarioVuelo(EntityModel):
    usuario = ForeignKeyField(Usuario)
    vuelo = ForeignKeyField(Vuelo, on_delete='cascade')

class Comentarios(EntityModel):
    descripcion = CharField()
    calificacion = DoubleField()
    fecha_creacion = DateTimeField(default = datetime.datetime.now)
    fecha_modificacion = DateTimeField(default = datetime.datetime.now)
    usuario  = ForeignKeyField(Usuario)
    vuelo = ForeignKeyField(Vuelo, on_delete='cascade')