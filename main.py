from html.parser import HTMLParser
from urllib.request import urlopen
import requests, lxml.html
import os, ssl

class CatParser(HTMLParser):
    """
    look for tags
    """
    def __init__(self,classname,classvalue):
        HTMLParser.__init__(self)    
        self.catagory = ''
        self.subjects = []
        self.grouping = {}
        self.final = {}
        self.target = ''
        self.recording = False
        self.li = False
        self.h3 = False
        self.clName = classname
        self.clValue = classvalue
        self.catlinks = {}
        self.links = []

    def handle_starttag(self, tag, attr):
        if self.li and tag == 'a':
            #append link to list
            self.links.append(attr[0][1])
        if tag == 'li':
            self.li = True
            return
        if tag == 'h3':
            self.h3 = True
            return

    def handle_endtag(self, tag):
        if tag == 'li':
            self.li = False
            return
        if tag == 'h3':
            self.h3 = False
            return
        if tag == 'ul':
            print('adding: '+self.catagory)
            self.final[self.catagory]=self.subjects
            self.catlinks[self.catagory] = self.links
            self.links = []
            self.subjects = []
            self.catagory = ''

    def handle_startendtag(self,tag,attr):
        if self.li:
            self.links.append(attr[1])
        if self.h3:
            self.subjectlinks.append(attr[1])

    def handle_data(self, data):
        if self.h3:
            self.catagory = data
        if self.li:
            self.subjects.append(data)
            return

def clean(string):
    """
    removes specified characters from a string
    """
    string = string.split()
    string = ''.join(string)
    string = string.split('\\')
    string = ''.join(string)
    return string[2:-2]

def cleaner(string):   
    string = string.split()
    string = ''.join(string)
    string = string.split('<')
    string = join(string)
    string = string.split('>')
    string = ''.join(string)
    string = string.split(' ')
    return string

def main():
    s = requests.session()

    """
    ssl certification
    """
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)): 
        ssl._create_default_https_context = ssl._create_unverified_context

    login = s.get('https://foundrycommerce.helpdocs.com/')
    login_html = lxml.html.fromstring(login.text)
    hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
    form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}

    form['password'] = 'orderforgehelp'

    response = s.post('https://foundrycommerce.helpdocs.com/login',data=form)

    clean_html = clean(response.text)

    userClass = str(input('Enter an html attribute (class, id, etc.):\n'))
    userValue = str(input("Enter the attribute's value:\n"))

    parser = CatParser(classname=userClass,classvalue=userValue)

    dict = {}
    dict_key = ''

    parser.feed(response.text)

    print(parser.subjects)



'''
from html.parser import HTMLParser
from urllib.request import urlopen#, urlencode
import requests, lxml.html
import os, ssl
from main import CatParser, clean, cleaner
s = requests.session()
login = s.get('https://foundrycommerce.helpdocs.com/')
login_html = lxml.html.fromstring(login.text)
hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
form['password'] = 'orderforgehelp'
response = s.post('https://foundrycommerce.helpdocs.com/login',data=form)
clean_html = clean(response.text)
dict = {}
dict_key = ''
parser = CatParser('class','section-header')
parser.feed(response.text)
print(parser.subjects)
'''

if '__name__' == '__main__':
    main()
   