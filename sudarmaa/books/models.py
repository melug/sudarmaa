from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'

class Book(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category)
    icon = models.ImageField(upload_to='book_icons')

    def __unicode__(self):
        return self.title

class Pick(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    order_number = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s %s, %s' % (self.user.username,
            self.book.title, self.order_number)

