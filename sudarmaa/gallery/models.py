from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from photologue.models import Gallery as PGallery

class Gallery(PGallery):

    user = models.ForeignKey(User, verbose_name=_('User'))

    class Meta:
        verbose_name = _('Gallery')
        verbose_name_plural = _('Galleries')

#########################################
#               Signals                 #
#########################################

from django.db.models.signals import post_save
from django.dispatch import receiver
from gallery.models import Gallery

@receiver(post_save, sender=User)
def create_default_gallery(sender, **kwargs):
    user, created = kwargs['instance'], kwargs['created']
    if created:
        Gallery.objects.create(user=user, title=user.username, title_slug=user.username)

