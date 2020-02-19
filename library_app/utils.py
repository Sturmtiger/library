from time import time

from django.utils.text import slugify


def gen_slug(s):
    """
    Takes some model field value and makes a slug based on it.
    """
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + "-" + str(int(time()))


def join_params_for_pagination(request_get, left_ampersand=True):
    """
    Pops 'page' key and joins parameters.
    """
    request_get.pop("page", "")
    joined_params = request_get.urlencode()

    if joined_params and left_ampersand:
        joined_params = "&" + joined_params

    return joined_params
