from django.contrib import admin

from .models import Author, Book, Genre, PublisherCompany

admin.site.register(Genre)
admin.site.register(PublisherCompany)
admin.site.register(Author)
admin.site.register(Book)
