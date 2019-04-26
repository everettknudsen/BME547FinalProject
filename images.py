from pymodm import connect, MongoModel, fields, EmbeddedMongoModel
from users import User
from datetime import datetime

connect("mongodb+srv://bme_547_final_project:bme_547_final_project@"
        "bme547finalproject-gjnxe.mongodb.net/test?retryWrites=true")

class Images(EmbeddedMongoModel):
    user = fields.ReferenceField(User)
