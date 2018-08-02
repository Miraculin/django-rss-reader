from . import parser
import os
from rssReader.models import Channel,RssObject
import urllib.request as request
from django.conf import settings

def updateFeeds():
    #TODO: update feeds
    for channels in Channel.objects.all():
        pass
    parser.parseRss(os.path.join(settings.PROJECT_ROOT,'test_ANN.xml'))

def addFeed(feedURL):
    #TODO: add feed urls
    for url in Channel.objects.value_list("feedURL"):
        if feedURL==url:
            return "Feed already added"
    request.urlretrieve(feedURL, temp.xml)
    parse.parseRss(temp.xml,feedURL)

def removeFeed(feedURL):
    feeds=Channel.objects.filter(feedURL=feedURL)
    if feeds:
        feeds.delete()

def resetDatabase():
    Channel.objects.all().delete()
    RssObject.objects.all().delete()
