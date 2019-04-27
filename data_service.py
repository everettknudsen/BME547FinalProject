from images import Image
from users import User


def create_user(email: str) -> User:
    """
    This module will create a unique user in the user database. The primary key and organization
    is done by email. A unique email must be entered (uniqueness is checked in a different
    function).

    :param email: Takes an email entered by the user in the GUI login window.
    :return: Registers the user in the MongoDB with primary key as email.
    """
    user = User()
    user.email = email

    user.save()

    return user


def find_account_by_email(email: str) -> User:
    """
    Moudule to query the database and determine if a user with this email already
    exists within the database. If so, use this function to throw an error.

    :param email: Takes email parameter from the GUI input by user
    :return: returns user if the user exists
    """
    user = User.objects(email=email).first()

    return user

def register_image(active_user: User, file_name: str,
                   image_data: str,) -> Image:
    image = Image()

    image.file_name = file_name
    image.image_data = image_data

    image.save()

