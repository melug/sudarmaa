from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from books.models import Book, Category, AccessHistory, Page, Author

class HomeTests(TestCase):
    
    fixtures = [ 'views_test.json' ]

    def testHomePage(self):
        client = Client()
        response = client.get(reverse('home'))
        self.assertEquals(len(response.context['new_books']), 4)
        picked_book = Book.objects.get(pk=2)
        self.assertEquals(response.context['picked_books'][0], picked_book)

    def testCategoryPage(self):
        client = Client()
        response = client.get(reverse('books-in-category'))
        self.assertEquals(response.context['books'].count(), 4)
        response = client.get(reverse('books-in-category')+'?cat=7')
        self.assertEquals(response.context['books'].count(), 1)
        self.assertEquals(response.context['category'].id, 7)
        self.assertEquals(response.context['categories'].count(), Category.objects.count())
        response = client.get(reverse('books-in-category')+'?aut=1')
        author = Author.objects.get(pk=1)
        self.assertEquals(response.context['author'], author)

    def testLatestPage(self):
        client = Client()
        response = client.get(reverse('latest-books'))
        books = response.context['books']
        pbook = None
        for book in books:
            if pbook != None:
                self.assertTrue(pbook.added>book.added)
            else:
                pbook = book

    def testStaffPicksPage(self):
        client = Client()
        response = client.get(reverse('staff-picks'))
        books = response.context['books']
        book = Book.objects.get(pk=2)
        self.assertEquals(books[0], book)

    def testAuthorPage(self):
        client = Client()
        response = client.get(reverse('author-show', kwargs={'pk':1}))
        self.assertEquals(response.status_code, 200)
        response = client.get(reverse('author-show', kwargs={'pk':999999}))
        self.assertEquals(response.status_code, 404)

    def testHistoryPage(self):
        client = Client()
        response = client.get(reverse('history-list'))
        self.assertEquals(response.status_code, 302)
        user = User.objects.create_user('testuser', 'test@test.mn', 'testuser')
        client.login(username='testuser', password='testuser')
        response = client.get(reverse('history-list'))
        self.assertEquals(response.status_code, 200)
        response = client.get(reverse('read-page', kwargs={'pk':5}))
        self.assertEquals(response.status_code, 200)
        response = client.get(reverse('history-list'))
        accesshistory = AccessHistory.objects.get(user=user)
        self.assertEquals(accesshistory.page, Page.objects.get(pk=5))

