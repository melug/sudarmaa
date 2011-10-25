from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'

class Book(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category)
    icon = models.ImageField(upload_to='book_icons')
    creator = models.ForeignKey(User, null=True)
    description = models.TextField(blank=True)

    def top_pages(self):
        return self.page_set.filter(parent_page__isnull=True).order_by('siblings_order')

    def __unicode__(self):
        return self.title

class Page(models.Model):
    parent_page = models.ForeignKey('self', related_name='subpages', null=True, blank=True)
    book = models.ForeignKey(Book)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    siblings_order = models.IntegerField()
    
    def __unicode__(self):
        return self.title

class Pick(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    order_number = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s. %s' % (self.order_number, self.book.title)

