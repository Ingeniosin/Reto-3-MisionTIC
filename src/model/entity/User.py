from peewee import BooleanField, Model, CharField, DateTimeField
import datetime
from app import App as Application
from flask_login import UserMixin

class User(Model, UserMixin):
    name = CharField()
    email = CharField(unique = True, index = True)
    password = CharField()
    is_active = BooleanField()
    created_date = DateTimeField(default = datetime.datetime.now)


    class Meta:
        database = Application.__instance__.database.database
        db_table = "User"
        
    def is_active(self):
        return self.get_id