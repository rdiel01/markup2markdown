from html.parser import HTMLParser
from urllib.request import urlopen
import os, ssl

class MyHTMLParser(HTMLParser):
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


if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context

response = urlopen('https://foundrycommerce.helpdocs.com')

copy = ''

for i in response:
    copy += clean(str(i))

print(copy)

parser = MyHTMLParser()
parser.feed(copy)