from django.db import models

# Create your models here.

class Word(models.Model):
    word = models.CharField(max_length=255)
    explanation = models.TextField()
    is_suggestion = models.BooleanField(default=True)

    def __unicode__(self):
        return self.word

