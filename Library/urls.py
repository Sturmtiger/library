"""Library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("library.urls")),
    path("accounts/", include("users.urls")),
    re_path(r"^accounts/", include("allauth.urls")),
    re_path(r"^ratings/", include("library.custom_star_ratings.urls",
                                  namespace="ratings")),
    # DRF
    path('api/', include('library.api.urls')),
    re_path(r'^api-auth/', include('rest_framework.urls')),
    re_path(r'^api-auth-token/', obtain_auth_token),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
