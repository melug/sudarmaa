"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from books.models import Page, Book, Category

class UserMix(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.mn', 'testuser')

class PageTests(UserMix):

    def setUp(self):
        super(PageTests, self).setUp()
        self.category = Category.objects.create(title='Test category')
        self.book = Book.objects.create(title='Title - 1', \
            category=self.category, icon=None, creator=self.user, \
            description='Test description')
        self.page1 = Page.objects.create(parent_page=None, book=self.book,
        title='Chapter-1', content='Content - 1', siblings_order=1)
        self.page2 = Page.objects.create(parent_page=None, book=self.book,
        title='Chapter-2', content='Content - 2', siblings_order=2)
        self.page3 = Page.objects.create(parent_page=self.page1, book=self.book,
        title='Chapter-3', content='Content - 3', siblings_order=1)

    def test_page(self):
        self.assertEqual(set(self.book.top_pages()), set([self.page1, self.page2]))

    def test_next_prev(self):
        self.assertEqual(self.page1.next_page(), self.page2)
        self.assertEqual(self.page2.next_page(), None)

        self.assertEqual(self.page2.prev_page(), self.page1)
        self.assertEqual(self.page1.prev_page(), None)

        self.assertEqual(self.page3.prev_page(), None)
        self.assertEqual(self.page3.next_page(), None)

