import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()

import datetime

def today_year():
    return int(datetime.date.today().year)

class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Наименование категории')
    slug = models.SlugField(unique=True,
                            verbose_name='URL')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(
        validators=[
            MaxValueValidator(datetime.date.today().year),
            MinValueValidator(0)
        ])
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, related_name='genre')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='category'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    text = models.TextField(null=False, verbose_name='Отзыв')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name='Оценка',
    )

    class Meta:
        unique_together = ['author', 'title']
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.id}'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    text = models.TextField(verbose_name='Комментарий')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta:
        ordering = ['-pub_date']
