"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json

from django.test import TestCase, client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from books.models import Page, Book, Category, Shelf, DEFAULT_SHELVES

class UserMix(TestCase):
    
    fixtures = []
    
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

class PageTests(UserMix):

    def test_page(self):
        self.assertEqual(set(self.book.top_pages()), set([self.page1, self.page2]))

    def test_next_prev(self):
        self.assertEqual(self.page1.next_page(), self.page2)
        self.assertEqual(self.page2.next_page(), None)

        self.assertEqual(self.page2.prev_page(), self.page1)
        self.assertEqual(self.page1.prev_page(), None)

        self.assertEqual(self.page3.prev_page(), None)
        self.assertEqual(self.page3.next_page(), None)

class ShelfTests(UserMix):

    def setUp(self):
        super(ShelfTests, self).setUp()
        self.c = client.Client()
    
    def test_shelf_created(self):
        self.assertEqual(self.user.shelves.count(), 3)
        for shelf, title in zip(self.user.shelves.order_by('title'), sorted(DEFAULT_SHELVES)):
            self.assertEqual(shelf.title, title)

    def test_shelf_add(self):
        self.assertTrue(self.c.login(username='testuser', password='testuser'))
        shelf = self.user.shelves.all()[0]
        # Test adding to shelf
        r = self.send_receive_json(reverse('shelf-action'), \
            {'s': shelf.id, 'b': self.book.id, 'a':'add' })
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(shelf.books.count(), 1)
        r = self.send_receive_json(reverse('shelf-action'), \
            {'s': shelf.id, 'b': 99999, 'a':'add' })
        self.assertEqual(r['error'], 9)
        # Test remove from shelf
        r = self.send_receive_json(reverse('shelf-action'), \
            {'s': shelf.id, 'b': self.book.id, 'a':'remove' })
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(shelf.books.count(), 0)
        r = self.send_receive_json(reverse('shelf-action'), \
            {'s': shelf.id, 'b': 99999, 'a':'remove' })
        self.assertEqual(r['error'], 9)

    def send_receive_json(self, url, data):
        r = self.c.post(url, data=data)
        j = json.loads(r.content)
        return j
