from pymodm import fields, MongoModel, connect
import datetime
import logging

connect("mongodb+srv://bme_547_final_project:bme_547_final_project"
        "@bme547finalproject-gjnxe.mongodb.net/test?retryWrites=true")


class UserImages(MongoModel):
    """
    This is a class which initializes the data fields which will then be used to store
    all data in the MongoDB database.

    """
    email = fields.EmailField(required=True, primary_key=True)
    original_images = fields.ListField()
    he_images = fields.ListField()
    cs_images = fields.ListField()
    he_count = fields.IntegerField()
    cs_count = fields.IntegerField()
    log_count = fields.IntegerField()
    rev_count = fields.IntegerField()
    user_actions = fields.ListField()


def add_new_user(email):
    """
    This function initializes a user in the image database before any
    images are uploaded.
    :param email: Email argument input into the GUI
    :return:
    """
    user = UserImages(email=email,
                      he_count=0,
                      cs_count=0,
                      log_count=0,
                      rev_count=0
                      )
    user.save()
