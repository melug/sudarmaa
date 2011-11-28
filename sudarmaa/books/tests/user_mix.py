from django.test import TestCase
from django.contrib.auth.models import User
from books.models import Page, Book, Category

class UserMix(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.mn', 'testuser')
        self.category = Category.objects.create(title='Test category')
        self.book = Book.objects.create(title='Title - 1', \
            category=self.category, icon=None, creator=self.user, \
            description='Test description', status=2)
        self.page1 = Page.objects.create(parent_page=None, book=self.book,
        title='Chapter-1', content='Content - 1', siblings_order=1)
        self.page2 = Page.objects.create(parent_page=None, book=self.book,
        title='Chapter-2', content='Content - 2', siblings_order=2)
        self.page3 = Page.objects.create(parent_page=self.page1, book=self.book,
        title='Chapter-3', content='Content - 3', siblings_order=1)

