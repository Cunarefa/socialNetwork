from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserRegistrationView, LoginView, LogoutView, PostViewSet, LikeView, LikeAnalytic, UserActivity

router = DefaultRouter()


router.register('register', UserRegistrationView, basename='register')
router.register('posts', PostViewSet, basename='posts')
router.register('activity', UserActivity, basename='activity')

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('likes', LikeView.as_view(), name='likes'),
    path('analytics', LikeAnalytic.as_view()),
]

urlpatterns += router.urls
