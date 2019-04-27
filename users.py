import mongoengine
import datetime

from images import Image


class User(mongoengine.Document):
    email = mongoengine.EmailField(primary_key=True, required=True)
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    images = mongoengine.EmbeddedDocumentListField(Image)

    meta = {
        'db_alias': 'core',
        'collection': 'users'
    }
