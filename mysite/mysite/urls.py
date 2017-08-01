from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login
from data.views import home,index,summary,stockspage,stocksfiles,tables,serveFiles,remover

urlpatterns = [
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home, name='home'),
    url(r'^logged_in/$', index, name='index'),
    url(r'^yahooapi/$', summary, name='yahooapi'),
    url(r'^login/$', login, {'template_name': 'admin/login.html'}),
    url(r'^stocks/$', stockspage, name='stocks'),
    url(r'^stocksfiles/$', stocksfiles, name='stocksfiles'),
    url(r'^tables/$', tables, name='tables'),
    url(r'^table/(?P<stock>\w+)/(?P<table>\w+)/$$', serveFiles, name='serveFiles'),
    url(r'^remover/$', remover, name='remover'),
]
