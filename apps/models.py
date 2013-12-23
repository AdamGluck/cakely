from django.db import models
from django.core.validators import URLValidator

class User(models.Model):
    fb_id = models.BigIntegerField(null = True, blank = True, unique=True)
    email = models.EmailField()

class Link(models.Model):
    #used instead of URLField to take longer URLS
    #http://stackoverflow.com/questions/10052220/advantages-to-using-urlfield-over-textfield
    url = models.TextField(validators=[URLValidator()], unique=True)
    title = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)

class UserLink(models.Model):
    user = models.ForeignKey(User)
    link = models.ForeignKey(Link)
    upvoted = models.BooleanField(default=False)
    seen = models.DateTimeField(null=True, blank=True)

