from peewee import PostgresqlDatabase
from playhouse.postgres_ext import *

class Database:
    
    def __init__(self, dbName, dbUser, dbPassword, dbHost, dbPort):
        self.dbName = dbName
        self.dbUser = dbUser
        self.dbPassword = dbPassword
        self.dbHost = dbHost
        self.dbPort = dbPort

    def open(self):
        self.database = PostgresqlDatabase(self.dbName, user = self.dbUser, password = self.dbPassword, host = self.dbHost, port = self.dbPort)
        return self.database.connect()
