from src.database.Database import Database

class App(object):
    __instance__ = None

    def __init__(self):
        self.database = Database("MisionTicDb", "testAccount", "test4ccount", "juancamp.me", 5432)
        self.database.open()
        self.createTables()

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

    def __new__(cls):
        if App.__instance__ is None:
            App.__instance__ = object.__new__(cls)
        return App.__instance__