from django.test import TestCase
from books.templatetags.bbcode import spacify

values = (
    (' Hello buddy! ', '&nbsp;Hello buddy! '),
    (' Hello buddy! \n Hello buddy!', '&nbsp;Hello buddy! \n&nbsp;Hello buddy!'),
)

class TestSpacify(TestCase):

    def testSpacify(self):
        for i, e in values:
            self.assertEquals(spacify(i), e)

