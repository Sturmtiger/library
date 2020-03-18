from time import time


def gen_username_from_email(email):
    """
    Creates a unique username based on email.
    """
    username = email.split('@')[0] + str(int(time()))
    return username
