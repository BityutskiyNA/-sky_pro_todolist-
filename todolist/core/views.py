from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from django.contrib.auth import login, logout

from .models import User
from .serializers import UserCreateSerializer, UserUpdateSerialiser, LoginSerializer, UpdatePasswordSerializer
from rest_framework.response import Response

class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer

@method_decorator(csrf_exempt)
class UserLogonView(CreateAPIView):
    serializer_class = LoginSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def perform_create(self, serializer):
        user = serializer.save()
        login(request=self.request, user=user)

# @method_decorator(ensure_csrf_cookie)
@method_decorator(csrf_exempt)
class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerialiser
    permission_classes = [IsAuthenticated]


    def get_object(self):
        return self.request.user

    # @method_decorator(csrf_exempt)
    def destroy(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

@method_decorator(csrf_exempt)
class PasswordUpdateAPIView(UpdateAPIView):
    permission_classes =  [IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    def get_object(self):
        return self.request.user
