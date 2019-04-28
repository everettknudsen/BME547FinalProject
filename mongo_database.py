from pymodm import fields, MongoModel, connect
import datetime
import logging
from flask import Flask, jsonify


def global_init():
    connect("mongodb+srv://bme_547_final_project:bme_547_final_project"
            "@bme547finalproject-gjnxe.mongodb.net/test?retryWrites=true")


class UserImages(MongoModel):
    """
    This is a class which initializes the data
    fields which will then be used to store
    all data in the MongoDB database.
    For original_images, he_images..., the inputs will be
    a tuple containing the image name as a string and the image data
    also as a longer base64 string.

    """
    email = fields.EmailField(required=True, primary_key=True)
    original_images = fields.ListField()
    he_images = fields.ListField()
    cs_images = fields.ListField()
    lc_images = fields.ListField()
    rv_images = fields.ListField()
    he_count = fields.IntegerField()
    cs_count = fields.IntegerField()
    lc_count = fields.IntegerField()
    rv_count = fields.IntegerField()


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
                      lc_count=0,
                      rv_count=0)
    user.save()

    status_message = "User registered!"
    return status_message, 201


def get_user_data(email):
    """
    This function will pull all the data for a given user
    and put it into a dictionary which can then be used in other
    modules.
    :param email: Email input from the GUI.
    :return: returns the populated user_dictionary
    """
    try:
        user = UserImages.objects.raw({"_id": email}).first()
        user_dict = {
            'original_images': user.original_images,
            'he_images': user.he_images,
            'cs_images': user.cs_images,
            'log_images': user.lc_images,
            'rev_images': user.rv_images,
            'he_count': user.he_count,
            'cs_count': user.cs_count,
            'log_count': user.lc_count,
            'rev_count': user.rv_count,
            'user_actions': user.user_actions,
        }
        return user_dict, 200
    except UserImages.DoesNotExist:
        user_dict = "The user does not exist! " \
                    "Go back and register user!"
        return user_dict, 400


def new_image_added(email, upload_package):
    """
    This function will take in a dictionary which contains the
     image name, the image data, and, the processing action.
     It will then.
    :param image_dict: A dictionary from the post request
    that contains the image name, the image data, and the processing
    action to be performed.
    :return:
    """

    try:
        user = UserImages.objects.raw({"_id": email}).first()
    except UserImages.DoesNotExist:
        new_user = add_new_user(email)
        logging.debug(new_user)

    image_name = upload_package["img_name"]
    image_data = upload_package["img_data"]
    image_size = upload_package["img_size"]
    timestamp = upload_package["timestamp"]

    orig_data_list = [image_name, image_data, image_size, timestamp]

    try:
        user.original_images.append(orig_data_list)
    except AttributeError:
        user.original_images = orig_data_list

    user.save()
    return "Successful upload!", 201


def new_image_added_pro(email, upload_package):
    """
    This function will take in a dictionary which contains the
     processed image name, the processed image data, and, the processing
     action. It will then save the processed image data to the correct
     field in the MongoDB.
    :param email: Email corresponding to the user.
    :param upload_package:  A dictionary from the post request
    that contains the processed image name, the processed image data, and
    the processing action to be performed.
    :return: A status message and a status code.
    """

    try:
        user = UserImages.objects.raw({"_id": email}).first()
    except UserImages.DoesNotExist:
        new_user = add_new_user(email)
        logging.debug(new_user)

    image_name = upload_package["img_name"]
    processed_data = upload_package["img_data_processed"]
    processed_size = upload_package["img_size_processed"]
    process_type = upload_package["process_type"]
    timestamp = upload_package["timestamp"]
    latency = upload_package["latency"]

    processed_data_list = [image_name, processed_data, processed_size,
                           timestamp, latency]

    if process_type == 'he':
        user.he_count += 1
        try:
            user.he_images.append(processed_data_list)
        except AttributeError:
            user.he_images = processed_data_list
    elif process_type == 'cs':
        user.cs_count += 1
        try:
            user.cs_images.append(processed_data_list)
        except AttributeError:
            user.cs_images = processed_data_list
    elif process_type == 'lc':
        user.lc_count += 1
        try:
            user.lc_images.append(processed_data_list)
        except AttributeError:
            user.lc_images = processed_data_list
    elif process_type == 'rv':
        user.rv_count += 1
        try:
            user.rv_images.append(processed_data_list)
        except AttributeError:
            user.rv_images = processed_data_list
    else:
        return "Invalid!", 500

    user.save()
    return "Successful upload!", 201


def normal_images(email):
    """This function simply returns the listField of normal images for a user

    Args:
        email (string): user email for ID

    Returns:
        mongo_image_list (listField): all uploaded non-processed images for
        user
    """
    # gets database for this user
    user = UserImages.objects.raw({"_id": email}).first()
    # extract image_list
    print(type(user.original_images))
    return user.original_images
