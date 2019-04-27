import mongoengine
import datetime


class TimeLatency(mongoengine.EmbeddedDocument):
    time_latency = mongoengine.ListField(required=True)

    meta = {
        'db_alias': 'core',
        'collection': 'time_latency'
    }
