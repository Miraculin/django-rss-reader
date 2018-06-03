from lxml import etree
import lxml.html
import urllib.request
import urllib.parse
import json
import os
from datetime import datetime
from rssReader.models import Channel,RssObject
testDoc = '/PROJECT_ROOT/test_ars.xml'
testDoc2 = '/PROJECT_ROOT/test_ANN.xml'

storyStore = []
contentCache = {}

def parseXml(doc):
    tree = etree.parse(doc)
    root = tree.getroot()
    channel = root.find("channel")
    dateText = channel.find("lastBuildDate").text
    lastDatetime = datetime.strptime(dateText, '%a, %d %b %Y %H:%M:%S %z')
    channelObj = Channel(title=channel.find("title"), link=channel.find("link"), desc=channel.find("description"), lastDate=lastDatetime)
    channelObj.save()
    items = root.findall(r".//item")
    for child in items:
        title = child.find("title").text
        link = child.find("link").text
        desc = child.find("description").text
        dateText = child.find("pubDate").text
        date = datetime.strptime(dateText, '%a, %d %b %Y %H:%M:%S %z')
        if child.find("{http://purl.org/rss/1.0/modules/content/}encoded") != None:
            content = child.find("{http://purl.org/rss/1.0/modules/content/}encoded").text
        elif link not in contentCache:
            content = parseHtmlContent(link)
            contentCache.update({link:content})
        else:
            content = contentCache[link]
        tempObject = RssObject(title=title, link=link, desc=desc, pubDate=date, content=content, channel=channelObj)
        tempObject.save()
        storyStore.append(tempObject)
    return storyStore

def parseHtmlContent(doc):
    urlOpen = urllib.request.build_opener()
    tree = lxml.html.parse(urlOpen.open(doc))
    root = tree.getroot()
    body = root.find_class("KonaBody")[0]
    content = ""
    match = body.find(r".//img")
    if match!=None:
        image = imageNetlink(doc, match)
        content = "<p><img src={} class=\"splash\"></p>".format(image)
    text = ""
    for p in body.findall(r".//p"):
        for img in p.findall(r".//img"):
            image = imageNetlink(doc, img)
            newImg = lxml.html.fromstring("<img src={}>".format(image))
            p.replace(img,newImg)
        text+=lxml.html.tostring(p).decode("utf-8")
    content+=text
    return content

def imageNetlink(doc, elm):
    if r"data-src" in elm.attrib:
        print(elm.get(r"data-src"))
        image = urllib.parse.urljoin(doc, elm.get("data-src"))
    else:
        image = urllib.parse.urljoin(doc, elm.get("src"))
    return image

if(__name__ == "__main__"):
    parseXml(testDoc2)
    print(storyStore[0].parseContent())
    print("Parse Success")
