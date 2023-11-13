from django.contrib import admin
from apps.book.models import Book
from apps.book.models import Genre
from apps.book.models import Rate
from apps.book.models import Author


admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Rate)
admin.site.register(Author)
