from lxml import etree
import lxml.html
import urllib.request
import urllib.parse
import json
import os
from . import html_utils
from datetime import datetime
from rssReader.models import Channel,RssObject
import bleach

testDoc = '/PROJECT_ROOT/test_ars.xml'
testDoc2 = '/PROJECT_ROOT/test_ANN.xml'



def parseRss(doc):
    tree = etree.parse(doc)
    root = tree.getroot()
    ns = root.nsmap
    channel = root.find("channel")
    dateText = channel.find("lastBuildDate").text
    lastDatetime = datetime.strptime(dateText, '%a, %d %b %Y %H:%M:%S %z')
    fields = {'desc': channel.find("description").text,
              'lastDate':lastDatetime}
    channelObj,created = Channel.objects.update_or_create(title=channel.find("title").text, link=channel.find("link").text,defaults=fields)
    items = root.findall(r".//item")
    for child in items:
        title = child.find("title").text
        link = child.find("link").text
        desc = child.find("description").text
        dateText = child.find("pubDate").text
        if dateText!=None:
            date = datetime.strptime(dateText, '%a, %d %b %Y %H:%M:%S %z')
        if ("content" in  ns) and (child.find("content:encoded",ns) != None):
            content = child.find("content:encoded",ns).text
        else:
            content = parseHtmlContent(link)
        imglink=parseSplashImage(link,channelObj.title)
        if imglink == None:
            imglink = "http://localhost"
        fields = {'desc': desc,
                  'content':content,
                  'splash':imglink}
        article,created = RssObject.objects.get_or_create(title=title, link=link, pubDate=date,channel=channelObj, defaults=fields)

def parseHtmlContent(doc):
    urlOpen = urllib.request.build_opener()
    tree = lxml.html.parse(urlOpen.open(doc))
    root = tree.getroot()
    content = ""
    for p in root.findall(r".//p"):
        for img in p.findall(r".//img")[1:]:
            image = html_utils.imageNetlink(doc, img)
            newImg = lxml.html.fromstring("<img src={}>".format(image))
            p.replace(img,newImg)
        content+=lxml.html.tostring(p).decode("utf-8")
    content=bleach.clean(content)
    return content

def parseSplashImage(doc, channelTitle):
    urlOpen = urllib.request.build_opener()
    tree = lxml.html.parse(urlOpen.open(doc))
    root = tree.getroot()
    if "Anime News Network" in channelTitle:
        ANN_body = root.find_class("KonaBody")[0]
        match = ANN_body.find(r".//img")
        if match!=None:
            image = html_utils.imageNetlink(doc,match)
            return image
        for p in root.findall(r".//p"):
            for img in p.findall(r".//img"):
                image = html_utils.imageNetlink(doc, img)
                return image
    else:
        image = root.find(r".//img")
        return image
