from django.contrib import admin
from books.models import Category, Book, Pick, Page, AccessHistory, Author

def make_published(modeladmin, request, queryset):
    queryset.update(status=2)

make_published.short_description = "Mark selected books as published"

def staff_pick(modeladmin, request, queryset):
    for book in queryset:
        if book.pick_set.count()==0:
            Pick.objects.create(user=request.user, book=book)

def staff_unpick(modeladmin, request, queryset):
    Pick.objects.filter(book__in=queryset).delete()

staff_pick.short_description = 'Set books picked by staff'
staff_unpick.short_description = 'Set books unpicked by staff'   

class BookAdmin(admin.ModelAdmin):
    actions = [ make_published, staff_pick, staff_unpick ]
    list_filter = ('status',)

admin.site.register(Book, BookAdmin)

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Pick)
admin.site.register(Page)
admin.site.register(AccessHistory)
