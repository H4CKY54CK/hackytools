import requests

def whatsmyip(arg1=None):
    if arg1:
        print(arg1)
    return requests.get('https://api.ipify.org').text

def icanhazip():
    return requests.get('https://ipv4.icanhazip.com').text.strip()
