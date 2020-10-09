import requests
import begin
from functools import wraps
import sys
import logging

def logme(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        logging.basicConfig(format="(%(levelname)s) %(asctime)s: %(message)s", filename=sys.modules['__main__'].__file__ + '.log', level=logging.DEBUG, datefmt="%D %r")
        try:
            result = function(*args, **kwargs)
            logging.debug(f"func: {function.__name__} | args: {args} | kwargs: {kwargs} | returned: {result}")
        except Exception as e:
            logging.debug(f"EXCEPTION: {e}")
            raise e
        return result
    return wrapper

@begin.start
def whatsmyip():
    return requests.get('https://api.ipify.org').text
