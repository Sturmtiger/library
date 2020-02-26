from django.contrib import admin
from .models import Author, Book, Genre, PublisherCompany, BookAuthorsPriority


class BookAuthorsPriorityInline(admin.TabularInline):
    model = BookAuthorsPriority


class BookAdmin(admin.ModelAdmin):
    inlines = [
        BookAuthorsPriorityInline,
    ]


admin.site.register(Genre)
admin.site.register(PublisherCompany)
admin.site.register(Author)
admin.site.register(BookAuthorsPriority)

admin.site.register(Book, BookAdmin)
