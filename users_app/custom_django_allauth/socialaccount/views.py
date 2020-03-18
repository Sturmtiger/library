from django.http import Http404


def login_cancelled(request):
    raise Http404
