from html.parser import HTMLParser
from urllib.request import urlopen, urlencode
import os, ssl

class MyHTMLParser(HTMLParser):
    """
    look for tags
    """
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)

def clean(string):
    """
    removes specified characters from a string
    """
    return string[2:-2]

"""
ssl certification
"""
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context

url = '*****'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
values = {'password':'******'}
headers = {'User-Agent' : user_agent}

data = urllib.urlencode(values)
req = urllib2.Request(url, data, headers)
response = urlopen(req)

copy = ''

for i in response: # step through bytes in object, clean out /b and /n, concat to blank string
    copy += clean(str(i))

print(copy)

parser = MyHTMLParser()
parser.feed(copy)