from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from djangoratings.fields import RatingField
from djangoratings.models import Vote

#########################################
#             BookManager               #
#########################################
class PublishManager(models.Manager):
    
    def get_query_set(self):
        return super(PublishManager, self).get_query_set().filter(status=2)

# Create your models here.
class Category(models.Model):

    title = models.CharField(_('name'), max_length=255)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

class Author(models.Model):
    
    first_name = models.CharField(_('First name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last name'), max_length=30, blank=True)
    email = models.EmailField(_('E-mail address'), blank=True)
    biography_short = models.CharField(_('Biography short'), max_length=100)
    biography = models.TextField(_('Biography'), blank=True)
    image = models.ImageField(_('Image'), upload_to='author_icons')
    # the user who added author information,
    # only the user can edit.
    user = models.ForeignKey(User, null=True, verbose_name=_('User'))

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')

STATUS_CHOICES = (
    (1, _('Draft')),
    (2, _('Published')),
    (3, _('Violates terms'))
)

LANGUAGE_CHOICES = (
    (1, _('Mongolia')),
    (2, _('English')),
)

class Book(models.Model):

    added = models.DateTimeField(_('Added date'), auto_now_add=True)
    category = models.ForeignKey(Category, verbose_name=_('Category'))
    creator = models.ForeignKey(User, null=True, verbose_name=_('Sender'))
    description = models.TextField(_('Description'), blank=True)
    icon = models.ImageField(_('Icon'), upload_to='book_icons', null=True)
    rating = RatingField(_('Rating'), range=5)
    status = models.IntegerField(_('Status'), choices=STATUS_CHOICES, default=1)
    title = models.CharField(_('Title'), max_length=255)
    authors = models.ManyToManyField(Author, related_name='books', verbose_name=_('Authors'))
    language = models.IntegerField(_('Language'), choices=LANGUAGE_CHOICES)
    
    objects = models.Manager()
    publish = PublishManager()

    def is_published(self):
        return self.status == 2

    def top_pages(self):
        return self.page_set.filter(parent_page__isnull=True).order_by('siblings_order')

    def count_rating(self):
        book_type = ContentType.objects.get_for_model(self)
        return Vote.objects.filter(content_type__pk=book_type.id, 
            object_id=self.id).count()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')

class Page(models.Model):

    parent_page = models.ForeignKey('self', related_name='subpages', null=True, blank=True)
    book = models.ForeignKey(Book, verbose_name=_('Book'))
    title = models.CharField(_('Title'), max_length=255)
    content = models.TextField(_('Content'), blank=True)
    siblings_order = models.IntegerField(_('Order'))

    def sibling_pages(self):
        if self.parent_page is not None:
            return self.parent_page.subpages
        else:
            return self.book.page_set

    def next_page(self):
        ''' returns next page in the section or None if not available '''
        try:
            return self.sibling_pages().filter(siblings_order__gt=self.siblings_order).\
                order_by('siblings_order')[0]
        except IndexError:
            return None
    
    def prev_page(self):
        ''' returns prev page in the section or None if not available '''
        try:
            return self.sibling_pages().filter(siblings_order__lt=self.siblings_order).\
                order_by('-siblings_order')[0]
        except IndexError:
            return None

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

class Pick(models.Model):

    user = models.ForeignKey(User, verbose_name=_('User'))
    book = models.ForeignKey(Book, verbose_name=_('Book'))
    order_number = models.IntegerField(_('Order'), default=0)

    def __unicode__(self):
        return '%s. %s' % (self.order_number, self.book.title)

    class Meta:
        verbose_name = _('Pick')
        verbose_name_plural = _('Picks')

class Bookmark(models.Model):

    user = models.ForeignKey(User, verbose_name=_('User'))
    added = models.DateTimeField(_('Added date'), auto_now_add=True)
    page = models.ForeignKey(Page, verbose_name=_('Page'))

    def __unicode__(self):
        return self.user.username + ":" + self.page.title

    class Meta:
        verbose_name = _('Bookmark')
        verbose_name_plural = _('Bookmarks')

class Shelf(models.Model):

    title = models.CharField(_('Title'), max_length=255)
    user = models.ForeignKey(User, related_name='shelves', verbose_name=_('User'))
    books = models.ManyToManyField(Book, verbose_name=_('Books'))
    is_public = models.BooleanField(default=True, verbose_name=_('Is public'))

    def __unicode__(self):
        return self.user.username + ':' + self.title

    def books_count(self):
        return self.books.filter(status=2).count()

    def books_published(self):
        return self.books.filter(status=2)

    class Meta:
        verbose_name = _('Shelf')
        verbose_name_plural = _('Shelves')

#########################################
#               Signals                 #
#########################################
from django.db.models.signals import post_save
from django.dispatch import receiver

DEFAULT_SHELVES = ('read', 'to-read', 'currently-reading')

@receiver(post_save, sender=User)
def create_default_shelves(sender, **kwargs):
    user, created = kwargs['instance'], kwargs['created']
    if created:
        for shelve_title in DEFAULT_SHELVES:
            shelf = Shelf.objects.create(title=shelve_title, user=user)

