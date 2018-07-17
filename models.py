from django.db import models

# Create your models here.
class Channel(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    desc = models.CharField(max_length=200)
    lastDate = models.DateTimeField()
    class Meta:
        unique_together = ["title", "link"]

class RssObject(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    desc = models.CharField(max_length=200)
    pubDate = models.DateTimeField()
    content = models.TextField()
    splash = models.URLField()
    channel = models.ForeignKey('Channel',on_delete=models.CASCADE)
    class Meta:
        unique_together = ["title", "link","channel","pubDate"]
