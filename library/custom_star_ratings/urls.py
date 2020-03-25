from __future__ import unicode_literals

from django.conf.urls import url
from star_ratings import app_settings

from .views import CustomRate

urlpatterns = [
    url(
        r"(?P<content_type_id>\d+)/(?P<object_id>"
        + app_settings.STAR_RATINGS_OBJECT_ID_PATTERN
        + ")/",
        CustomRate.as_view(),
        name="rate",
    )
]

app_name = "star_ratings"
