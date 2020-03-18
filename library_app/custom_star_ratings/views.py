from star_ratings.views import *


class CustomRate(Rate):
    """
    Checks whether the user is the publisher of the book
    and prohibits access to voting.
    """
    def post(self, request, *args, **kwargs):
        if request.is_ajax() and not app_settings.STAR_RATINGS_ANONYMOUS:
            if request.user.is_authenticated:
                book = self.get_object()
                user = request.user
                if user.profile.publisher_company == book.publisher_company:
                    result = {'errors': 'Publisher cannot rate their book'}
                    res_status = 400
                    return JsonResponse(data=result, status=res_status)

        return super().post(request, *args, **kwargs)
