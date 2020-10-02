import requests

def whatsmyip():
    return requests.get('https://api.ipify.org').text
