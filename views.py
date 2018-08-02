from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import datetime
from . import urls
from . import feedManager
from . import html_utils as utils
from lxml import etree
from django.conf import settings
from rssReader.models import Channel,RssObject

from django.views.decorators.cache import never_cache

import time

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><h1> It is now %s.</h1><body>It's a pretty cool time to be alive</body></html>" % now
    return HttpResponse(html)

def index(request):
    url_list = urls.urlpatterns
    template = loader.get_template('rssReader/index.html')
    context = {"url_list":url_list}
    return HttpResponse(template.render(context, request))

@never_cache
def testArticle(request):
    print(time.perf_counter())
    #feedManager.resetDatabase()
    feedManager.updateFeeds()
    print(time.perf_counter())
    articles = RssObject.objects.all()#[:25][::-1]
    print(time.perf_counter())
    template = loader.get_template('rssReader/articles.html')
    print(time.perf_counter())
    context = {"article_list":articles}
    print("Successful")
    return HttpResponse(template.render(context,request))
