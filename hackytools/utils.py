import sys
import requests
import socket

def whatsmyip():
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['local', '-local', '--local']:
            return socket.gethostbyname(socket.gethostname())
    return requests.get('https://api.ipify.org').text.strip()

def icanhazip():
    return requests.get('https://ipv4.icanhazip.com').text.strip()
