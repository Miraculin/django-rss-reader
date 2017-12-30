from lxml import etree
import lxml.html
import urllib.request
import urllib.parse
import json
import os

testDoc = '/PROJECT_ROOT/test_ars.xml'
testDoc2 = '/PROJECT_ROOT/test_ANN.xml'


storyStore = []
content_cache = {}
class Channel:
    '''class representing the source channel'''

    def __init__(self, title, link, desc, lastDate):
        self.title = title
        self.link = link
        self.desc = desc
        self.lastDate = lastDate

class RssObject:
    '''Object to represent a parsed \"story\"'''

    def __init__(self,  title, link, desc, pubDate, content, channel):
        self.title = title
        self.link = link
        self.desc = desc
        self.pubDate = pubDate
        self.content = content
        self.channel = channel

    def testPrint(self):
        print(self.content)

    def getTitle(self):
        return self.title

    def getLink(self):
        return self.link

    def getDesc(self):
        return self.desc

    def getPubDate(self):
        return self.pubDate

    def getContent(self):
        htmlDoc = self.content
        return(htmlDoc)

def parseXml(doc):
    tree = etree.parse(doc)
    root = tree.getroot()
    channel = root.find("channel")
    channelObj = Channel(channel.find("title"), channel.find("link"), channel.find("description"), channel.find("lastBuildDate"))
    items = root.findall(r".//item")
    for child in items:
        title = child.find("title").text
        link = child.find("link").text
        desc = child.find("description").text
        date = child.find("pubDate").text
        if child.find("{http://purl.org/rss/1.0/modules/content/}encoded") != None:
            content = child.find("{http://purl.org/rss/1.0/modules/content/}encoded").text
        elif link not in content_cache:
            content = parseHtmlContent(link)
            content_cache.update({link:content})
        else:
            content = content_cache[link]
        tempObject = RssObject( title, link, desc, date, content, channelObj)
        storyStore.append(tempObject)
    return storyStore

def parseHtmlContent(doc):
    urlOpen = urllib.request.build_opener()
    tree = lxml.html.parse(urlOpen.open(doc))
    root = tree.getroot()
    body = root.find_class("KonaBody")[0]
    content = ""
    for imageElement in body.findall(r".//img"):
        if r"data-src" in imageElement.attrib:
            print(imageElement.get(r"data-src"))
            image = urllib.parse.urljoin(doc, imageElement.get("data-src"))
        else:
            image = urllib.parse.urljoin(doc, imageElement.get("src"))
        content = "<p><img src={} class=\"splash\"></p>".format(image)
    text = ""
    for p in body.findall(r".//p"):
        #TODO: find img fix their path
        text+=lxml.html.tostring(p).decode("utf-8")
    content+=text
    return content

if(__name__ == "__main__"):
    parseXml(testDoc2)
    print(storyStore[0].parseContent())
    print("Parse Success")
