import requests
import begin

@begin.start
def whatsmyip():
    return requests.get('https://api.ipify.org').text
