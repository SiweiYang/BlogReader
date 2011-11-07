import logging

from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf


from google.appengine.api import taskqueue

from BlogSpider import BlogParser, ArticleListParser, ArticleParser
from BlogModel import Blog, BlogForm, Article

def index(request):
    blogs = Blog.all().order('-url')
    blog_list = [(target.author,target.key()) for target in blogs]
    
    return render_to_response('blog_list.html', {'blog_list':blog_list})
    
def article(request, id):
    article = Article.get(id)
    
    if not article.content:
        target = ArticleParser.ArticleParser(article.url)
        target.process()
        logging.info('Loading new article from %s' % target.url)
        logging.info('Loading new article : %s' % target.title)
        
        article.content = target.get_content()
        article.put()
    
    return render_to_response('article.html', {'article':article})

def new_blog(request):
    form = {'blog_form':BlogForm()}
    form.update(csrf(request))
    return render_to_response('new_blog.html', form)
    
def add_blog(request):
    if request.method == 'POST': # If the form has been submitted...
        form = BlogForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            bloger = Blog(author = form.cleaned_data['author'],service_provider = form.cleaned_data['service_provider'],url = form.cleaned_data['url'])
            bloger.put()
            return redirect('/blog/%s' % bloger.key()) # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return redirect('/new_blog/')

    
def blog(request, id):
    bloger = Blog.get(id)
    if not bloger:
        return render_to_response('article_list.html', {'article_list':[]})
    
    logging.info('Loading bloger : %s' % bloger.author)
    blog = BlogParser.BlogParser(bloger.url)
    blog.process()
    
    articles = []
    url = blog.getArticleListUrl()
    while True:
        logging.info('Loading article list : %s' % url)
        articleList = ArticleListParser.ArticleListParser(url)
        articleList.process()
        articles.extend(articleList.articleList)
        
        url = articleList.nextPage()
        if not url:
            break
        else:
            if Article.all().filter('url =', articles[-1]['url']).get():
                break
    
    list = []
    for article in articles:
        item = Article.all().filter('url =', article['url']).get()
        if not item:
            item = Article(blog=bloger,url=article['url'],title=article['title'])
            item.put()
            
            # Add the task to the default queue.
            taskqueue.add(url='/article/%s' % item.key())

        list.append((item.title,item.key()))
    
    # Mark this update time
    bloger.put()
    return render_to_response('article_list.html', {'article_list':list})
    
def blog_default(request):
    bloger = Blog.all().filter('url =', 'http://blog.sina.com.cn/sjxxh').get()
    if not bloger:
        bloger = Blog(author = 'Monkeyking',service_provider = 'sina',url = 'http://blog.sina.com.cn/sjxxh')
        bloger.put()
    
    return blog(request, bloger.key())