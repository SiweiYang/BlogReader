from google.appengine.ext import db

from django import forms

class Blog(db.Model):
    author = db.StringProperty(required=True)
    service_provider = db.StringProperty(required=True, choices=set(['sina']))
    last_update = db.DateTimeProperty(auto_now=True, auto_now_add=True)
    url = db.StringProperty(required=True)

class BlogForm(forms.Form):
    author = forms.CharField(max_length=100, required=True)
    service_provider = forms.CharField(max_length=10, required=True)
    url = forms.URLField(required=True)

    
class Article(db.Model):
    url = db.StringProperty(required=True)
    blog = db.ReferenceProperty(Blog)
    title = db.StringProperty(required=True)
    content = db.TextProperty()
    