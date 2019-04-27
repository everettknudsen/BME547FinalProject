import mongoengine
import datetime


class Image(mongoengine.EmbeddedDocument):
    file_name = mongoengine.StringField(primary_key=True, required=True)
    image_data = None
    meta = {
        'db_alias': 'core',
        'collection': 'users'
    }
