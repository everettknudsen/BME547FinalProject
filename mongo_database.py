from pymodm import fields, MongoModel, connect
from pymongo import MongoClient

import datetime
import logging
from flask import Flask, jsonify


db = ''
client = ''


def global_init():
    global client, db
    connect("mongodb+srv://bme_547_final_project:bme_547_final_project"
            "@bme547finalproject-gjnxe.mongodb.net/test?retryWrites=true")
    client = MongoClient("mongodb+srv://bme_547_final_project:bme_"
                         "547_final_project@bme547finalproject-gjnxe."
                         "mongodb.net/test?retryWrites=true")
    db = client.test


class users(MongoModel):
    """
    This is a class which initializes the data
    fields which will then be used to store
    all data in the MongoDB database.
    For original_images, he_images..., the inputs will be
    a tuple containing the image name as a string and the image data
    also as a longer base64 string.

    """
    email = fields.CharField(required=True, primary_key=True)
    original_images = fields.ListField()
    processed_images = fields.ListField()
    he_count = fields.IntegerField()
    cs_count = fields.IntegerField()
    lc_count = fields.IntegerField()
    rv_count = fields.IntegerField()


def check_if_user_registered(email):
    try:
        user = users.objects.raw({"_id": email}).first()
        user_status = True
        return user_status
    except users.DoesNotExist:
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
    user = users(email=email,
                 he_count=0,
                 cs_count=0,
                 lc_count=0,
                 rv_count=0)
    user.save()
    return "User registered!"


def get_one_user(email):
    """
    This function will pull all the data for a given user
    and put it into a dictionary which can then be used in other
    modules.
    :param email: Email input from the GUI.
    :return: returns the populated user_dictionary
    """
    try:
        user = db.users.find_one({"_id": email})
        # print('current user is', user)
        return user
    except users.DoesNotExist:
        user = "DNE"

        # print('current user is', user)
        return user


def print_users():
    active_users = db.users
    for one_user in active_users.find():
        print("Active Users:", one_user)


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
        user = get_one_user(email)
    except user == "DNE":
        user = add_new_user(email)
        logging.debug(user)

    try:
        original_images = user['original_images']
        name = upload_package['img_name']
        original_images.append(upload_package)
        db.users.update({'_id': email,
                         'original_images.img_name': {'$ne': name}},
                        {'$push': {'original_images': original_images}})

        print_users()
    except KeyError:
        print('first image')
        original_images = [upload_package]
        print(type(original_images))
        db.users.update({'_id': email},
                        {'$push': {'original_images': original_images}},
                        upsert=True)
        print('current user is', user)

    return "Successful upload!"


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
        user = get_one_user(email)
    except user == "DNE":
        user = add_new_user(email)
        logging.debug(user)

    try:
        processed_images = user['processed_images']
        processed_images.append(upload_package)
        db.users.update({'_id': email},
                        {'$addToSet': {'processed_images': processed_images}})
    except KeyError:
        processed_images = [upload_package]
        db.users.update({'_id': email},
                        {'$push': {'processed_images': processed_images}},
                        upsert=True)

    process_type = upload_package['process_type']

    if process_type == 'he':
        he_count = user['he_count']
        he_count += 1
        db.users.update({'_id': email},
                        {'$set': {'he_count': he_count}})
    elif process_type == 'cs':
        cs_count = user['cs_count']
        cs_count += 1
        db.users.update({'_id': email},
                        {'$set': {'cs_count': cs_count}})
    elif process_type == 'lc':
        lc_count = user['lc_count']
        lc_count += 1
        db.users.update({'_id': email},
                        {'$set': {'lc_count': lc_count}})
    elif process_type == 'rv':
        rv_count = user['rv_count']
        rv_count += 1
        db.users.update({'_id': email},
                        {'$set': {'rv_count': rv_count}})
    else:
        return "Invalid Process!", 500

    return "Successful upload!"


def normal_images(email):
    """This function simply returns the listField of normal images for a user

    Args:
        email (string): user email for ID

    Returns:
        mongo_image_list (listField): all uploaded non-processed images for
        user
    """
    # gets database for this user
    user = get_one_user(email)
    image_list = user['original_images']

    # extract image_list
    print('\n\n mongo side type of list', type(image_list))
    return image_list
