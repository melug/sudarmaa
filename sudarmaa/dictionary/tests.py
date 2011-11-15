from django.core.urlresolvers import reverse

from django.test import TestCase
from django.test.client import Client

from dictionary.models import Word


class DictionaryTest(TestCase):
    fixtures = [ 'fixtures/test_words.json' ]

    def setUp(self):
        self.client = Client()

    def test_found(self):
        response = self.client.get(reverse('get-word'), {'w': 'zany'})
        zany = Word.objects.get(word='zany')
        self.assertEqual(response.context['status'], 'found')
        self.assertEqual(response.context['word'], zany)

    def test_suggestion(self):
        response = self.client.get(reverse('get-word'), {'w': 'ze'})
        self.assertEqual(response.context['status'], 'suggestion')
        self.assertEqual(len(response.context['suggestions']), 5)

    def test_notfound(self):
        response = self.client.get(reverse('get-word'), {'w': 'alyusha'})
        self.assertEqual(response.context['status'], 'notfound')

