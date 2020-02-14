from django.db import models


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
    title = models.CharField(max_length=50)
    cover = models.ImageField(null=True, blank=True)
    year_made = models.PositiveSmallIntegerField()
    page_count = models.PositiveSmallIntegerField()
    publisher_company = models.ForeignKey(
        PublisherCompany, related_name="books", on_delete=models.CASCADE
    )
    authors = models.ManyToManyField("Author", related_name="books")
    genres = models.ManyToManyField("Genre", related_name="books")


class Author(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, null=True, blank=True)
    pseudonym = models.CharField(max_length=50, unique=True)
    birthday = models.DateField()
    deathday = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=50)
    biography = models.TextField()
    genres = models.ManyToManyField("Genre", related_name="authors")

    def __str__(self):
        return self.pseudonym
