from lxml import etree
import lxml.html
import bleach
import urllib.parse

def imageNetlink(doc, elm):
    if r"data-src" in elm.attrib:
        image = urllib.parse.urljoin(doc, elm.get("data-src"))
    else:
        image = urllib.parse.urljoin(doc, elm.get("src"))
    return image

def truncateContent(content):
    max_length=1000
    return content
    # if len(content)<=max_length:
    #     return content
    # else:
    #     bleached = bleach.clean(content,tags=['p'],strip=True)
    #     root = lxml.html.fromstring(bleached)
    #     paragraphs = root.findall(r".//p")
    #     return bleached
