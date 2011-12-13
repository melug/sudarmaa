import datetime

from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, client

from books.models import Book

class TestEpubGenerator(TestCase):

    fixtures = [ "fixtures/book_test.json" ]

    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.mn', 'testuser')

    def testEpubDownload(self):
        self.client = client.Client()
        self.client.login(username='testuser', password='testuser')
        r = self.client.get(reverse('download-page', kwargs={'pk':5}))
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.context['object'].id, 5)
        r = self.client.get(reverse('download-book', kwargs={'pk':5}))
        self.assertEquals(r.status_code, 200)

    def testEpubMethod(self):
        book = Book.objects.get(id=5)
        self.assertEquals(book.epub_creation, None)
        self.assertEquals(book.epub_file, '')
        self.assertEquals(book.get_epub_file(), settings.BOOKS_DIR+'/5.epub')
        self.assertIsNotNone(book.epub_creation)
        self.assertIsNotNone(book.epub_file, '5.epub')
        self.assertEquals(book.get_epub_file(), settings.BOOKS_DIR+'/5.epub')
        self.assertEquals(book.get_epub_file(), settings.BOOKS_DIR+'/5.epub')

