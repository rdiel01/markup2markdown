#from confluence.client import Confluence
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
        if self.record and tag and attr:
            self.body += '<{0} {1}="{2}">'.format(tag,attr[0][0],attr[0][1])
            return
        if self.record and tag:
            self.body += '<{0}>'.format(tag)
            return
       

    # def handle_startendtag(self, tag, attr):
    #     #need to add img tag info
    #     if self.record:
    #         self.body += '<{0}>'.format(tag)
    #         # for x in attr:
    #         #     if x[0] == 'src':
    #         #         self.body += x[0]+'="'+x[1]+'">'

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
        self.ul = False
        self.catlinks = {}
        self.links = []

    def handle_starttag(self, tag, attr):
        if self.li and self.ul and tag == 'a':
            #append link to list
            self.links.append(attr[0][1])
        if tag == 'li':
            self.li = True
            return
        if tag == 'ul' and attr:
            if attr[0][1] == 'articles-list':
                print(attr)
                self.ul = True
                return

    def handle_endtag(self, tag):
        if tag == 'li':
            self.li = False
            return
        if tag == 'ul':
            self.ul = False
            return
    '''    
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
        if self.ul:
            self.subjectlinks.append(attr[1])
            return
    
    def handle_data(self, data):
        
        if self.ul:
            self.catagory = data
        
        if self.li:
            self.subjects.append(data)
            return
    '''

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

    userPass = input("enter password for foundry commerce help docs:")

    form['password'] = str(userPass)

    signin = s.post('https://foundrycommerce.helpdocs.com/login',data=form)

    response = s.get('https://foundrycommerce.helpdocs.com/categories')

    parser = CatParser()
    '''
    dict = {}
    dict_key = ''
    '''
    parser.feed(response.text)

    return parser.links

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
        for titleLink in link_dictionary[key]:
            login = s.get('https://foundrycommerce.helpdocs.com/')
            login_html = lxml.html.fromstring(login.text)
            hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
            form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
            form['password'] = 'orderforgehelp'

            response = s.post('https://foundrycommerce.helpdocs.com/login',data=form)
            page = s.get(titleLink[1])
            html_body.feed(page.text)
            #creat new word doc named after catagory and index number
            f = open('final/'+key+'_'+titleLink[0]+'.txt',"x")
            f.write(html_body.body)
            f.close()
            html_body.body=''
            i += 1

def catSplit(list):
    """
    takes list, returns dict, 
    """
    dict = {}
    for url in list:
        urlSplit = url.split('/')
        category = urlSplit[3]
        titleLink = (urlSplit[4],'https:'+url)
        if category not in dict.keys():
            dict[category] = [titleLink]
        else:
            dict[category].append(titleLink)
    return dict

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
    #f = open("test_doc.txt", "x")
    category_links = link_grab()
    category_dict = catSplit(category_links)
    link_user(category_dict)
    """
    for i in category_links:
        f.write(i)
        for j in category_links[i]:
            f.write(j)
    f.close()
    """

if '__name__' == '__main__':
    main()

