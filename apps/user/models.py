from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    saved_books = models.ManyToManyField('book.Book', blank=True)
