from django.contrib import admin
from books.models import Category, Book, Pick, Page, Shelf

def make_published(modeladmin, request, queryset):
    queryset.update(status=2)

make_published.short_description = "Mark selected books as published"

def staff_pick(modeladmin, request, queryset):
    for book in queryset:
        if book.pick_set.count()==0:
            Pick.objects.create(user=request.user, book=book)

staff_pick.short_description = 'Set books picked by staff'
    

class BookAdmin(admin.ModelAdmin):
    actions = [ make_published, staff_pick ]

admin.site.register(Book, BookAdmin)

admin.site.register(Category)
admin.site.register(Pick)
admin.site.register(Page)
admin.site.register(Shelf)
