from django.dispatch import receiver
from django.db.models.signals import post_save

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from .models import Book
from comments_app.models import Comment


@receiver(post_save, sender=Book)
def reset_book_detail_cache(sender, instance, **kwargs):
    """
    Reset the cache of a specific book uf it has been edited.
    """
    book_slug = instance.slug
    key = make_template_fragment_key('book_detail', [book_slug])
    cache.delete(key)


@receiver(post_save, sender=Comment)
def reset_book_detail_cache_comments(sender, instance, **kwargs):
    """
    Reset the cache of a specific book if it has been commented.
    """
    commented_model = instance.content_type.model_class()
    if commented_model is Book:
        related_book = instance.book.first()
        book_slug = related_book.slug
        key = make_template_fragment_key('book_detail', [book_slug])
        cache.delete(key)
