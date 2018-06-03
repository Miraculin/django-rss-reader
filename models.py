from django.db import models

# Create your models here.
class Channel(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    desc = models.CharField(max_length=200)
    lastDate = models.DateTimeField()

class RssObject(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    desc = models.CharField(max_length=200)
    pubDate = models.DateTimeField()
    content = models.TextField()
    channel = models.ForeignKey('Channel',on_delete=models.CASCADE)
