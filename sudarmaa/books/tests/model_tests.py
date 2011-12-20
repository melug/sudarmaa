import json

from django.test import TestCase, client
from django.core.urlresolvers import reverse
from books.models import Page, Book, Category
from books.tests.user_mix import UserMix

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

