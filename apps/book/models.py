from django.db import models
from apps.common.models import SEO


class Author(models.Model):
    name = models.TextField('ФИО')

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField('Название')

    def __str__(self):
        return self.name


class Book(SEO):
    name = models.TextField('Название')
    description = models.TextField('Описание')
    genres = models.ManyToManyField('Genre')
    authors = models.ManyToManyField('Author')
    published_date = models.DateField('Дата публикации')

    def __str__(self):
        return self.name


class Rate(models.Model):
    user = models.ForeignKey('user.User', models.CASCADE)
    book = models.ForeignKey('Book', models.CASCADE)
    rate = models.PositiveSmallIntegerField('Оценка', default=0)
    text = models.TextField('Текст отзыва')
