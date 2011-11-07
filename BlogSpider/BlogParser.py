#!/usr/bin/env python
from urllib2 import urlopen
from HTMLParser import HTMLParser

class BlogParser(HTMLParser):
    def __init__(self, url):
        HTMLParser.__init__(self)
        self.url = url
        self.lines = []
        self.mode = None
        self.path = []
        self.urls = []
        
        page = urlopen(url).readlines()
        
        for line in page:
            line = line.strip()
            if line == '<!\xe2\x80\x93[if lte IE 6]>' or line == '<![endif]\xe2\x80\x93>' or line == '':
                    continue
            self.lines.append(line)
    def process(self):
        for line in self.lines:
            #print line
            self.feed(line.decode('utf-8'))
            self.feed('\n')
        #self.close()
    def getArticleListUrl(self):
        if len(self.urls) == 4:
            return self.urls[1]
    def handle_startendtag(self, tag, attrs):
        #print tag
        pass
    def handle_starttag(self, tag, attrs):
        if tag == 'div' and attrs == [('class', 'blognavInfo')]:
            self.mode = 'blognavInfo'
        if self.mode =='blognavInfo':
            self.path.append(tag)
        if self.mode =='blognavInfo' and self.path == ['div','span','a']:
            for attr in attrs:
                if attr[0] == 'href':
                    self.urls.append(attr[1])
    def handle_endtag(self, tag):
        if self.mode == 'blognavInfo':
            self.path.pop()
            if len(self.path) == 0:
                self.mode = None
        pass

if __name__ == '__main__':
    parser = BlogParser('http://blog.sina.com.cn/sjxxh')
    parser.process()
    print parser.getArticleListUrl()
