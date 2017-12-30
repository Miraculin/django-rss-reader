from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import datetime
from . import urls
from . import testParser
from lxml import etree
import os
from django.conf import settings

from django.views.decorators.cache import never_cache

# Create your views here.

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><h1> It is now %s.</h1><body>It's a pretty cool time to be alive</body></html>" % now
    return HttpResponse(html)

def index(request):
    url_list = urls.urlpatterns
    template = loader.get_template('Reader/index.html')
    context = {"url_list":url_list}
    return HttpResponse(template.render(context, request))

@never_cache
def testArticle(request):
    articles = testParser.parseXml(os.path.join(settings.PROJECT_ROOT,'test_ANN.xml'))
    article_list = []
    with open(os.path.join(settings.PROJECT_ROOT,'articles.txt'),"a") as f:
        for article in articles:
            if not(article.getContent() in article_list):
                article_list.append("<h2>{}</h2>".format(article.getTitle())+article.getContent())
                f.write("{}\n".format("<h2>{}</h2>".format(article.getTitle())+article.getContent()))
    template = loader.get_template('Reader/articles.html')
    context = {"article_list":article_list}
    print(article_list)
    return HttpResponse(template.render(context,request))
