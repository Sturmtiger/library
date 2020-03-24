from allauth.socialaccount.views import ConnectionsView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


def login_cancelled(request):
    raise Http404


class CustomConnectionsView(LoginRequiredMixin, ConnectionsView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.GET.get("next", "/")
        return context
