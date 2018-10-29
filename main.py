from html.parser import HTMLParser
from urllib.request import urlopen#, urlencode
import requests, lxml.html
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
    string = string.split()
    string = ''.join(string)
    string = string.split('\\')
    string = ''.join(string)
    return string[2:-2]

s = requests.session()

"""
ssl certification
"""
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context

login = s.get('****')
login_html = lxml.html.fromstring(login.text)
hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
print(login.url)
print(form)

form['password'] = '***'
response = s.post('****',data={'password':''***})

print(response.url)

'''
url = ''
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
values = {'password':''}
headers = {'User-Agent' : user_agent}

#data = urllib.urlencode(values)
#req = urllib2.Request(url, data, headers)
response = urlopen(url)

copy = ''

for i in response: # step through bytes in object, clean out /b and /n, concat to blank string
    copy += clean(str(i))

print(copy)

#print(response.info())

parser = MyHTMLParser()
parser.feed(copy)
'''