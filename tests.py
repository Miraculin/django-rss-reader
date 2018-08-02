from django.test import TestCase
from rssReader.models import Channel,RssObject

class RssObject(TestCase):
    def setUp(self):
        Channel.objects.create()
# Create your tests here.
