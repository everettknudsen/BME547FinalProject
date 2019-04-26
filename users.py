from pymodm import connect, MongoModel, fields
from datetime import datetime


def init_mongo_db():
    connect("mongodb+srv://bme_547_final_project:bme_547_final_project@bme547finalproject-gjnxe.mongodb.net/test?retryWrites=true")


class User(MongoModel):
    email = fields.EmailField(primary_key=True, required=True)
    images = fields.EmbeddedDocumentListField()