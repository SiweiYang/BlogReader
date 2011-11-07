#!/usr/bin/env python
from urllib2 import urlopen
from HTMLParser import HTMLParser
from StringIO import StringIO

class ArticleParser(HTMLParser):
    def __init__(self, url):
        HTMLParser.__init__(self)
        self.url = url
        self.lines = []
        self.mode = None
        self.path = []
        self.title = ''
        self.content = StringIO()
        
        page = urlopen(url).readlines()
        for line in page:
            line = line.strip()
            if line == '<!\xe2\x80\x93[if lte IE 6]>' or line == '<![endif]\xe2\x80\x93>' or line == '':
                    continue
            
            self.lines.append(line.decode('utf-8'))
    def get_content(self):
        return self.content.getvalue()
        
    def process(self):
        for line in self.lines:
            #print line
            content = ''
            if self.mode == 'content':
                content = line
            self.feed(line)
            self.feed('\n')
            if self.mode == 'content':
                print >> self.content, content
        #self.close()
    def handle_data(self, data):
        if self.mode == 'article' and self.path == ['div','div','h2']:
            self.title += data.strip()
        pass
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for attr in attrs:
                if attr == ('id', 'articlebody'):
                    self.mode = 'article'
                    self.path = []
        if self.mode == 'article' or self.mode == 'content':
            if tag == 'wbr':
                return
            self.path.append(tag)
            if self.path == ['div','div']:
                for attr in attrs:
                    print attr
                    if attr[0].strip() == 'class' and attr[1].strip() == 'articalContent':
                        self.mode = 'content'
        pass
    def handle_endtag(self, tag):
        if self.mode == 'article' or self.mode == 'content':
            self.path.pop()
            if len(self.path) == 1:
                self.mode = 'article'
            if len(self.path) == 0:
                self.mode = None
        pass
    
if __name__ == '__main__':
    parser = ArticleParser('http://blog.sina.com.cn/s/blog_593b23560100s1ka.html')
    parser.process()
    print parser.title
    print parser.get_content()