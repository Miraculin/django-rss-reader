from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import datetime
from . import urls
from . import parser
from . import html_utils as utils
from lxml import etree
import os
from django.conf import settings
from rssReader.models import Channel,RssObject

from django.views.decorators.cache import never_cache

# Create your views here.

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
    parser.parseRss(os.path.join(settings.PROJECT_ROOT,'test_ANN.xml'))
    articles = RssObject.objects.all()[:25]
    template = loader.get_template('rssReader/articles.html')
    context = {"article_list":articles}
    print("Successful")
    return HttpResponse(template.render(context,request))
