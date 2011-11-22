from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
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
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'

STATUS_CHOICES = (
    (1, 'Draft'),
    (2, 'Published'),
    (3, 'Violates terms')
)

class Book(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category)
    icon = models.ImageField(upload_to='book_icons', null=True)
    creator = models.ForeignKey(User, null=True)
    description = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    rating = RatingField(range=5)
    
    objects = models.Manager()
    publish = PublishManager()

    def top_pages(self):
        return self.page_set.filter(parent_page__isnull=True).order_by('siblings_order')

    def count_rating(self):
        book_type = ContentType.objects.get_for_model(self)
        return Vote.objects.filter(content_type__pk=book_type.id, 
            object_id=self.id).count()

    def __unicode__(self):
        return self.title

class Page(models.Model):
    parent_page = models.ForeignKey('self', related_name='subpages', null=True, blank=True)
    book = models.ForeignKey(Book)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    siblings_order = models.IntegerField()

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

class Pick(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    order_number = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s. %s' % (self.order_number, self.book.title)

class Shelf(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='shelves')
    books = models.ManyToManyField(Book)
    is_public = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user.username + ':' + self.title

    class Meta:
        verbose_name_plural = 'Shelves'

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
            Shelf.objects.create(title=shelve_title, user=user)

