import mongoengine
import datetime

from images import Image
from time_latency import TimeLatency


class Metrics(mongoengine.EmbeddedDocument):
    file_name = mongoengine.ReferenceField(Image, primary_key=True)
    processing_type = mongoengine.StringField(default='original',
                                              required=True)
    image_size = mongoengine.FloatFieldField(required=True)
    time_latency = mongoengine.EmbeddedDocumentListField(required=True)

    meta = {
        'db_alias': 'core',
        'collection': 'metrics'
    }
