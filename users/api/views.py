from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework import permissions

from .serializers import SignUpSerializer, UserProfileSerializer


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer


class UserProfileView(RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
