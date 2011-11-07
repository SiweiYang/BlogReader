#!/usr/bin/env python
from urllib2 import urlopen
from exceptions import Exception
from HTMLParser import HTMLParser

class ArticleListParser(HTMLParser):
    def __init__(self, url):
        HTMLParser.__init__(self)
        self.url = url
        self.lines = []
        self.mode = None
        self.path = []
        self.articleList = []
        self.pageList = []
        
        for i in range(3):
            try:
                page = urlopen(url).readlines()
                break
            except Exception:
                if i < 2:
                    continue
                raise
                
        
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
    def nextPage(self):
        for page in self.pageList:
            if page > self.url:
                return page
    def handle_data(self, data):
        if self.mode == 'articleList' and self.path == ['div','div','p','span','a']:
            self.articleList[-1]['title'] = data.strip()
        pass
    def handle_starttag(self, tag, attrs):
        if tag == 'div' and attrs == [('class', 'articleList')]:
            self.mode = 'articleList'
            self.path = []
        if self.mode == 'articleList':
            self.path.append(tag)
        if self.mode == 'articleList' and self.path == ['div','div','p','span','a']:
            for attr in attrs:
                if attr[0] == 'href':
                    self.articleList.append({'url':attr[1]})
        
        if tag == 'div' and attrs == [('class', 'SG_page')]:
            self.mode = 'pageList'
            self.path = []
        if self.mode == 'pageList':
            self.path.append(tag)
        if self.mode == 'pageList' and self.path == ['div','ul','li','a']:
            for attr in attrs:
                if attr[0] == 'href':
                    self.pageList.append(attr[1])
            
            
        pass
    def handle_endtag(self, tag):
        if self.mode == 'articleList' or self.mode == 'pageList':
            self.path.pop()
            if len(self.path) == 0:
                self.mode = None
        pass

if __name__ == '__main__':
    parser = ArticleListParser('http://blog.sina.com.cn/s/articlelist_1497047894_0_1.html')
    parser.process()
    print parser.articleList
    print parser.nextPage()
