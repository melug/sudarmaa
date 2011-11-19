from django.contrib import admin
from books.models import Category, Book, Pick, Page, Shelf

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Pick)
admin.site.register(Page)
admin.site.register(Shelf)
