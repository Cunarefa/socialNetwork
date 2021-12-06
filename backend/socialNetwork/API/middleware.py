from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.exceptions import InvalidToken

from .models import User


class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            auth_result = authentication.JWTAuthentication().authenticate(request)
        except InvalidToken:
            return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        if auth_result:
            request.user = auth_result[0]

        if request.user.is_authenticated:
            User.objects.filter(id=request.user.id).update(last_activity=timezone.now())
