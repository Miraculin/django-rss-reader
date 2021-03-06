from lxml import etree
import lxml.html
import urllib.request as request
import urllib.parse
import json
import os
from . import html_utils
from datetime import datetime
from rssReader.models import Channel,RssObject
import bleach
from django.core.files import File

testDoc = '/PROJECT_ROOT/test_ars.xml'
testDoc2 = '/PROJECT_ROOT/test_ANN.xml'

def parseRss(doc, feedURL = None):
    tree = etree.parse(doc)
    root = tree.getroot()
    ns = root.nsmap
    channel = root.find("channel")
    dateText = channel.find("lastBuildDate").text
    lastDatetime = datetime.strptime(dateText, '%a, %d %b %Y %H:%M:%S %z')
    if feedURL is not None:
        chfields = {'desc': channel.find("description").text,
                'lastDate':lastDatetime,
                'feedURL':feedURL}
    else:
        chfields = {'desc': channel.find("description").text,
                'lastDate':lastDatetime,
                }
    channelObj,created = Channel.objects.update_or_create(title=channel.find("title").text, link=channel.find("link").text,defaults=chfields)
    items = root.findall(r".//item")
    print(items)
    for child in items:
        title = child.find("title").text
        link = child.find("link").text
        desc = child.find("description").text
        dateText = child.find("pubDate").text
        if dateText!=None:
            date = datetime.strptime(dateText, '%a, %d %b %Y %H:%M:%S %z')
        article,created = RssObject.objects.get_or_create(title=title, link=link, pubDate=date,channel=channelObj)
        if not created:
             break
        if ("content" in  ns) and (child.find("content:encoded",ns) != None):
            content = child.find("content:encoded",ns).text
        else:
            content = parseHtmlContent(link,channelObj.title)
        imglink=parseSplashImage(link,channelObj.title)
        if imglink != None:
            result=request.urlretrieve(imglink)
            img = File(open(result[0],mode='rb'))
            article.splash.save(title+" splash", img)
        fields = {'desc': desc,
                  'content':content,
                  }
        for(k,v) in fields.items():
            setattr(article, k, v)
        article.save()

def parseHtmlContent(doc,channelTitle):
    urlOpen = request.build_opener()
    tree = lxml.html.parse(urlOpen.open(doc))
    root = tree.getroot()
    content = ""
    tags_list=['p','img','li','ul','ol','b','i']
    if "Anime News Network" in channelTitle:
        ANN_body=root.find_class("KonaBody")[0]
        if ANN_body.find(r".//p")==None:
            content="<p>"+lxml.html.tostring(ANN_body).decode("utf-8")+"</p>"
            return bleach.clean(content,tags=tags_list,strip=True)
    for p in root.findall(r".//p"):
        for img in p.findall(r".//img"):
            image = html_utils.imageNetlink(doc, img)
            newImg = lxml.html.fromstring("<img src={}>".format(image))
            img.getparent().replace(img,newImg)
        content+=lxml.html.tostring(p).decode("utf-8")
    content=bleach.clean(content,tags=tags_list,strip=True)
    return content

def parseSplashImage(doc, channelTitle):
    urlOpen = request.build_opener()
    tree = lxml.html.parse(urlOpen.open(doc))
    root = tree.getroot()
    match = root.find(r".//img")
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
