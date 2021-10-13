from src.database.Database import Database

class App(object):
    __instance__ = None

    def __init__(self):
        self.database = Database("MisionTicDb", "testAccount", "test4ccount", "juancamp.me", 5432)
        print("database")
        self.database.open()
        self.createTables()

    def createTables(self):
        from src.model.entity.User import User
        if not User.table_exists():
                User.create_table()

    def __new__(cls):
        if App.__instance__ is None:
            App.__instance__ = object.__new__(cls)
        return App.__instance__