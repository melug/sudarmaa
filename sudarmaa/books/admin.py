from django.contrib import admin
from books.models import Category, Book, Pick

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Pick)
