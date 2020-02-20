from django.db import models
from .utils import gen_slug


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
    authors = models.ManyToManyField("Author",
                                     related_name="books",
                                     through="BookAuthorsPriority")
    genres = models.ManyToManyField("Genre", related_name="books")

    def save(self, *args, **kwargs):
        self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}({self.id})'


class Author(models.Model):
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True)
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


class BookAuthorsPriority(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    main = models.BooleanField(default=False)
