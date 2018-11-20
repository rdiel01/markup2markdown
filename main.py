from html.parser import HTMLParser
from urllib.request import urlopen
import requests, lxml.html
import os, ssl

class PageParser(HTMLParser):
#used to find body of help doc
    def __init__(self):
        HTMLParser.__init__(self)    
        self.bodylist = []
        self.body = ''
        self.record = False
    
    def handle_starttag(self, tag, attr):
        if tag == 'header' and attr[0][1] == 'article-header':
            self.body += '<{0} {1}="{2}"'.format(tag,attr[0][0],attr[0][1])
            self.record = True
            return
        if self.record and tag:
            self.body += '<{0}>'.format(tag)
            return
        if self.record and tag and attr:
            self.body += '<{0} {1}="{2}"'.format(tag,attr[0][0],attr[0][1])
            return

    def handle_endtag(self, tag):
        if self. record and tag == 'section':
            self.body += '</section>'
            self.record = False
            return
        if self.record:
            self.body += '</{0}>'.format(tag)
 
    def handle_data(self, data):
        if self.record:
            self.body += data
            return


class CatParser(HTMLParser):
    """
    look for tags
    """
    def __init__(self):
        HTMLParser.__init__(self)    
        self.catagory = ''
        self.subjects = []
        self.final = {}
        self.li = False
        self.h3 = False
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
            return

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

def link_grab():
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

    parser = CatParser()

    dict = {}
    dict_key = ''

    parser.feed(response.text)

    return parser.catlinks

def link_user(link_dictionary):
    # uses PageParser to find help doc info and save to its own text doc.
    s = requests.session()

    """
    ssl certification
    """
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)): 
        ssl._create_default_https_context = ssl._create_unverified_context
    
    html_body = PageParser()
    for key in link_dictionary:
        i=0
        for link in link_dictionary[key]:
            login = s.get('https://foundrycommerce.helpdocs.com/')
            login_html = lxml.html.fromstring(login.text)
            hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
            form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
            form['password'] = 'orderforgehelp'

            response = s.post('https://foundrycommerce.helpdocs.com/login',data=form)
            page = s.get('https:'+link)
            html_body.feed(page.text)
            #creat new word doc named after catagory and index number
            f = open('z_'+key+'_'+str(i)+'.txt',"x")
            f.write(html_body.body)
            f.close()
            html_body.body=''
            i += 1

def main():
    #f = open("test_doc.txt", "x")
    catagory_links = link_grab()
    link_user(catagory_links)
    """
    for i in catagory_links:
        f.write(i)
        for j in catagory_links[i]:
            f.write(j)
    f.close()
    """

if '__name__' == '__main__':
    main()


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