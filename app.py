from logging import log
from src.database.Database import Database

class App(object):
    __instance__ = None

    def __init__(self):
        self.database = Database("MisionTicDb", "testAccount", "test4ccount", "juancamp.me", 5432)
        self.database.open()
        self.createTables()

    def __new__(cls):
        if App.__instance__ is None:
            App.__instance__ = object.__new__(cls)
        return App.__instance__

    def createTables(self):
        from src.model.Entity import Usuario, Rol, Lugar, Avion, Vuelo, UsuarioVuelo, Comentarios
        if not Rol.table_exists():
            Rol.create_table()
            Rol.create(nombre = "Usuario").save()
            Rol.create(nombre = "Piloto").save()
            Rol.create(nombre = "Administrador").save()
        if not Usuario.table_exists():
                Usuario.create_table()
        if not Lugar.table_exists():
                Lugar.create_table()
                lugares = [
                    {'nombre': 'Armenia'},
                    {'nombre': 'Barranquilla'},
                    {'nombre': 'Bogota'},
                    {'nombre': 'Bucaramanga'},
                    {'nombre': 'Cali'},
                    {'nombre': 'Cucuta'},
                    {'nombre': 'Cartagena'},
                    {'nombre': 'Leticia'},
                    {'nombre': 'Medellin'},
                    {'nombre': 'Pereira'},
                    {'nombre': 'San Andres'},
                    {'nombre': 'Santa Marta'},
                    {'nombre': 'Monteria'},
                    {'nombre': 'Pasto'},
                ]
                for data_dict in lugares:
                     Lugar.create(**data_dict).save()
        if not Avion.table_exists():
                Avion.create_table()
        if not Vuelo.table_exists():
                Vuelo.create_table()
        if not UsuarioVuelo.table_exists():
                UsuarioVuelo.create_table()
        if not Comentarios.table_exists():
                Comentarios.create_table()
        self.defaultRole = Rol.get_or_none(Rol.nombre == "Usuario")
        self.pilotRole = Rol.get_or_none(Rol.nombre == "Piloto") 
        self.adminRole = Rol.get_or_none(Rol.nombre == "Administrador")   
        self.lugares = [t for t in list(Lugar.select())]
        self.lugaresTouple = list(map(lambda x: (x.id, x.nombre), self.lugares))
        self.aviones = [t for t in list(Avion.select())] 
        self.avionesTouple = list(map(lambda x: (x.id, x.nombre), self.aviones))
        self.pilotos = [t for t in list(Usuario.select().where(Usuario.role == self.pilotRole))]
        self.pilotosTouple = list(map(lambda x: (x.id, x.nombre), self.pilotos))
        print("Loaded...")


    def getVuelos(self):
        from src.model.Entity import Vuelo
        return [t for t in list(Vuelo.select())]