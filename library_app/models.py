from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from star_ratings.models import Rating

from comments_app.models import Comment

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
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    cover = models.ImageField(null=True, blank=True)
    year_made = models.PositiveSmallIntegerField()
    page_count = models.PositiveSmallIntegerField()
    publisher_company = models.ForeignKey(
        PublisherCompany, related_name="books", on_delete=models.CASCADE)
    authors = models.ManyToManyField("Author",
                                     related_name="books",
                                     through="BookAuthorsPriority")
    genres = models.ManyToManyField("Genre", related_name="books")
    ratings = GenericRelation(Rating, related_query_name='books')
    comments = GenericRelation(Comment, related_query_name='books')

    def get_absolute_url(self):
        return reverse('library_app:book_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        print('BOOK SAVE')
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

    def get_absolute_url(self):
        return reverse('library_app:author_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = gen_slug(self.pseudonym)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.pseudonym


class BookAuthorsPriority(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    priority = models.PositiveSmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        print('PRIORITY SAVE')
        prev_same_book = BookAuthorsPriority.objects.filter(
            book=self.book).last()
        if prev_same_book:
            self.priority = prev_same_book.priority + 1
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('book', 'priority')
