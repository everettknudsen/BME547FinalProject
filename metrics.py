import mongoengine
import datetime

from images import Image


class Metrics(mongoengine.EmbeddedDocument):
    file_name = mongoengine.ReferenceField(Image, primary_key=True)
    date_registered = mongoengine.DateTimeField(datetime.datetime.now)
    processing_type = mongoengine.StringField(default='original',
                                              required=True)
    processing_time = mongoengine.FloatField(required=True)
    image_size = mongoengine.FloatField(required=True)

    meta = {
        'db_alias': 'core',
        'collection': 'metrics'
    }
