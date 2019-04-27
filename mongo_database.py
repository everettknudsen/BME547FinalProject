from pymodm import fields, MongoModel, connect
import datetime
import logging

connect("mongodb+srv://bme_547_final_project:bme_547_final_project"
        "@bme547finalproject-gjnxe.mongodb.net/test?retryWrites=true")


class UserImages(MongoModel):
    """
    This is a class which initializes the data
    fields which will then be used to store
    all data in the MongoDB database.

    """
    email = fields.EmailField(required=True, primary_key=True)
    original_images = fields.ListField()
    he_images = fields.ListField()
    cs_images = fields.ListField()
    log_images = fields.ListField()
    rev_images = fields.ListField()
    he_count = fields.IntegerField()
    cs_count = fields.IntegerField()
    log_count = fields.IntegerField()
    rev_count = fields.IntegerField()
    user_actions = fields.ListField()


def check_if_user_registered(email):
    try:
        user = UserImages.objects.raw({"_id": email}).first()
        user_status = True
        return user_status
    except UserImages.DoesNotExist:
        user_status = False
        return user_status


def add_new_user(email):
    """
    This function initializes a user in
    the image database before any
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

    status_message = "User registered!"
    return status_message, 200


def get_user_data(email):
    try:
        user = UserImages.objects.raw({"_id": email}).first()
        user_dict = {
            'original_images': user.original_images,
            'he_images': user.he_images,
            'cs_images': user.cs_images,
            'log_images': user.log_images,
            'rev_images': user.rev_images,
            'he_count': user.he_count,
            'cs_count': user.cs_count,
            'log_count': user.log_count,
            'rev_count': user.rev_count,
            'user_actions': user.user_actions,
        }
        return 200
    except UserImages.DoesNotExist:
        user_dict = "The user does not exist! " \
                    "Go back and register user!"
        return 400
