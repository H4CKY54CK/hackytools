import requests
import argparse
import begins

@begin.start
def whatsmyip():
    return requests.get('https://api.ipify.org').text