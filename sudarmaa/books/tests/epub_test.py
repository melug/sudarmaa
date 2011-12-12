from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase, client

class TestEpubGenerator(TestCase):

    fixtures = [ "fixtures/book_test.json" ]

    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.mn', 'testuser')

    def testEpub(self):
        self.client = client.Client()
        self.client.login(username='testuser', password='testuser')
        r = self.client.get(reverse('download-page', kwargs={'pk':5}))
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.context['object'].id, 5)
        r = self.client.get(reverse('download-book', kwargs={'pk':5}))
        self.assertEquals(r.status_code, 200)

