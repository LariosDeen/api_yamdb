from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(verbose_name='Дата выхода')
    category = models.ForeignKey(Category,
                                 verbose_name='Категория',
                                 related_name='titles',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    description = models.TextField('Описание произведения',
                                   null=True, blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle',
                                   verbose_name='Жанр')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.SET_NULL,
                              verbose_name='Произведение',
                              blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL,
                              verbose_name='Жанр',
                              blank=True, null=True)

    def __str__(self):
        return self.genre
