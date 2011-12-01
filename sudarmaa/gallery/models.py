from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from photologue.models import ImageModel

class MPhoto(ImageModel):

    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name='photos', null=True, verbose_name=_('User'))
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')

    def __unicode__(self):
        return self.title

