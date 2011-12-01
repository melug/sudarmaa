from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Word(models.Model):
    word = models.CharField(_('Word'), max_length=255)
    explanation = models.TextField(_('Explanation'))

    def __unicode__(self):
        return self.word

    class Meta:
        verbose_name = _('Word')
        verbose_name_plural = _('Words')

class Suggestion(models.Model):
    word = models.CharField(_('Word'), max_length=255)
    explanation = models.TextField(_('Explanation'))
    contributor = models.ForeignKey(User, null=True, verbose_name=_('Contributor'))
    date_added = models.DateTimeField(_('Date added'), auto_now_add=True)
    approved = models.BooleanField(_('Approved'), default=False)

    def __unicode__(self):
        return "{0} - {1}".format(self.contributor.username, self.word)

    class Meta:
        verbose_name = _('Suggestion')
        verbose_name_plural = _('Suggestions')

