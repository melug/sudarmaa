import json

from django.test import TestCase, client
from django.core.urlresolvers import reverse

from books.models import Page, Book, Category, Shelf, Bookmark, DEFAULT_SHELVES
from books.tests.user_mix import UserMix

class BookmarkTests(UserMix):

    def setUp(self):
        super(BookmarkTests, self).setUp()
        self.c = client.Client()

    def test_bookmark(self):
        self.assertTrue(self.c.login(username='testuser', password='testuser'))
        r = self.send_receive_json(reverse('bookmark-add', kwargs={'page_id':self.page1.id}), {})
        self.assertEqual(r['status'], 'ok')
        r = self.send_receive_json(reverse('bookmark-add', kwargs={'page_id':self.page1.id}), {})
        self.assertEqual(r['error'], 'already created')
        r = self.send_receive_json(reverse('bookmark-add', kwargs={'page_id':99999}), {})
        self.assertEqual(r['error'], 10)
        r = self.send_receive_json(reverse('bookmark-remove', kwargs={'page_id':self.page1.id}), {})
        self.assertEqual(r['status'], 'deleted')
        r = self.send_receive_json(reverse('bookmark-remove', kwargs={'page_id':self.page1.id}), {})
        self.assertEqual(r['error'], 10)

    def test_mybookmarks(self):
        self.assertTrue(self.c.login(username='testuser', password='testuser'))
        self.send_receive_json(reverse('bookmark-add', kwargs={'page_id':self.page1.id}), {})
        self.send_receive_json(reverse('bookmark-add', kwargs={'page_id':self.page2.id}), {})
        r = self.c.get(reverse('bookmark-index'))
        bookmarks = Bookmark.objects.filter(user=self.user)
        self.assertEqual(bookmarks.count(), 2)
        self.assertEqual(set(r.context['object_list']), set(bookmarks))

    def send_receive_json(self, url, data):
        r = self.c.post(url, data=data)
        j = json.loads(r.content)
        return j

