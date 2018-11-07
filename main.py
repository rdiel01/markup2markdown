from html.parser import HTMLParser
from urllib.request import urlopen#, urlencode
import requests, lxml.html
import os, ssl

class CatParser(HTMLParser):
    """
    look for tags
    """
    def __init__(self,classname,classvalue):
        HTMLParser.__init__(self)    
        #self.catagory = ''
        self.subjects = []
        #self.final = {}
        #self.target = ''
        self.recording = False
        self.clName = classname
        self.clValue = classvalue
        self.livedata = ''
    '''
    def hunt_for(self, tag, attr):
        if self.handle_starttag(tag, attr) == 'ul':
            self.lsSubjects.append(self.handle_data())
    '''
    def handle_starttag(self, tag, attr):
        for name,value in attr:
            if name == self.clName and value == self.clValue:
                self.recording = True
                print('START RECORDING')
    '''
            if name == self.clName and value = self.clValue:
            if self.tag == 'h3' and self.attr == :
            print('Start tag: ' + tag)
    '''
    def handle_endtag(self, tag):
        if tag == 'ul':
            self.recording = False
            print('DONE RECORDING')

    def handle_startendtag(self,tag,attr):
        if self.recording and tag == 'a':
            for name, value in attr:
                self.livedata = value


    def handle_data(self, data):
        while self.recording:
            self.subjects.append(data)
            print("ADDIND : ", data)
            self.recording = False


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


def h1_list():
    pass
'''
def search_for(list):
    for i in len(list):
        if list(i) == '<ul':
            for j in len(list[i+1:]):
                if list[j] == '<h3><a>'
                    dict_key = list[j+1]
                    continue
                if list[j] == '<li><a':
                    for word in list[j+1:]:
                        if word[-1] != '>':
                            dict[dict_key] = word
                            if word[-1] == '>':
                                dict[dict_key] += word[:-10]                    
                if list[j] == '</ul>':
                    continue
                
                if list(j+1) == None:
                    break
'''
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

    #print(clean_html)
    userClass = str(input('Enter an html attribute (class, id, etc.):\n'))
    userValue = str(input("Enter the attribute's value:\n"))

    parser = CatParser(classname=userClass,classvalue=userValue)
    # tag_detector = False

    dict = {}
    dict_key = ''

    parser.feed(response.text)

    print(parser.subjects)






   

    #parser.feed(list.text)


    '''
    url = ''
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    values = {'password':''}
    headers = {'User-Agent' : user_agent}

    #data = urllib.urlencode(values)
    #req = urllib2.Request(url, data, headers)
    list = urlopen(url)

    copy = ''

    for i in list: # step through bytes in object, clean out /b and /n, concat to blank string
        copy += clean(str(i))



    #print(list.info())

    parser = MyHTMLParser()
    parser.feed(copy)
    '''

if '__name__' == '__main__':
    main()
   