import requests

def rest_get_json(url):
    """Return the json portion of the REST GET.

    Return None if an exception was triggered.
    """

    response = None

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as error:
        pass # log error here

    status_OK = 200
    if hasattr(response, 'status_code') and \
       (response.status_code == status_OK):
        ret = response.json()
    else:
        ret = None

    return ret

def rest_put(url, value):
    """Put the new value to the bioreactor."""

    # I don't know the syntax for a put, so just printing here.
    print("Request to set {} on {}".format(value, url))

