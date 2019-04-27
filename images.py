import mongoengine
import datetime

from metrics import Metrics


class Image(mongoengine.EmbeddedDocument):
    file_name = mongoengine.StringField(primary_key=True, required=True)
    image_data = mongoengine.StringField(required=True)
    image_metrics = mongoengine.EmbeddedDocumentField(Metrics)

    meta = {
        'db_alias': 'core',
        'collection': 'users'
    }
