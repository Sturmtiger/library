from time import time

from django.db import models
from django.utils.text import slugify


def gen_slug(s):
    """
    Takes some model field value and makes a slug based on it.
    """
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + "-" + str(int(time()))


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class PublisherCompany(models.Model):
    name = models.CharField(max_length=50, unique=True)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Publisher companies"


class Book(models.Model):
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    title = models.CharField(max_length=50)
    cover = models.ImageField(null=True, blank=True)
    year_made = models.PositiveSmallIntegerField()
    page_count = models.PositiveSmallIntegerField()
    publisher_company = models.ForeignKey(
        PublisherCompany, related_name="books", on_delete=models.CASCADE
    )
    authors = models.ManyToManyField("Author", related_name="books")
    genres = models.ManyToManyField("Genre", related_name="books")

    def save(self, *args, **kwargs):
        self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)


class Author(models.Model):
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, null=True, blank=True)
    pseudonym = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(null=True, blank=True)
    birthday = models.DateField()
    deathday = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=50)
    biography = models.TextField()
    genres = models.ManyToManyField("Genre", related_name="authors")

    def save(self, *args, **kwargs):
        self.slug = gen_slug(self.pseudonym)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.pseudonym