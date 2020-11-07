import requests

def whatsmyip():
    return requests.get('https://api.ipify.org').text

def icanhazip():
    return requests.get('https://ipv4.icanhazip.com').text.strip()
