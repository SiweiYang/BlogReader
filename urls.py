from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^BlogReader/', include('BlogReader.foo.urls')),

    (r'^$', 'views.index'),
    
    (r'^new_blog', 'views.new_blog'),
    (r'^add_blog', 'views.add_blog'),
    (r'^blog$', 'views.blog_default'),
    (r'^blog/(?P<id>\w+)$', 'views.blog'),
    
    (r'^article/(?P<id>\w+)$', 'views.article'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
