from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Word(models.Model):
    word = models.CharField(max_length=255)
    explanation = models.TextField()

    def __unicode__(self):
        return self.word

class Suggestion(models.Model):
    word = models.CharField(max_length=255)
    explanation = models.TextField()
    contributor = models.ForeignKey(User, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        return "{0} - {1}".format(self.contributor.username, self.word)

