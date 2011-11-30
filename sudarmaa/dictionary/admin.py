from django.contrib import admin
from dictionary.models import Word, Suggestion

def accept_suggestion(modeladmin, request, queryset):
    for suggestion in queryset:
        Word.objects.get_or_create(word=suggestion.word,
            explanation=suggestion.explanation)
        suggestion.approved = True
        suggestion.save()

class SuggestionAdmin(admin.ModelAdmin):
    actions = [ accept_suggestion ]

admin.site.register(Word)
admin.site.register(Suggestion, SuggestionAdmin)
