from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone as tz

from Library.celery_app import app
from library.models import Book


@app.task(name="users.celery_tasks.send_mail_async")
def send_mail_async(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)


@app.task(name="users.celery_tasks.newsletter")
def newsletter():
    user_model = get_user_model()
    user_emails = list(
        user_model.objects.filter(profile__get_newsletter=True).values_list(
            "email", flat=True
        )
    )

    date_from = tz.now().date() - timedelta(days=5)
    new_books = Book.objects.filter(created_at__date__gte=date_from).order_by(
        "-created_at"
    )[:5]
    if new_books and user_emails:
        current_site = Site.objects.get_current()

        mail_context = {
            "new_books": new_books,
            "protocol": "http",
            "domain": current_site.domain,
        }

        subject = render_to_string("users/newsletter/subject.txt")
        message = render_to_string("users/newsletter/email.html", context=mail_context)

        send_mail_async.delay(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=user_emails,
        )
