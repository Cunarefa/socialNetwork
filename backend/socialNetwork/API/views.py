from django.contrib.auth.models import User, update_last_login
from django.db.models import Count
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Post, Like, User
from .serializers import UserRegistrationSerializer, PostSerializer, LikeSerializer, LikeAmountSerializer, \
    UserActivitySerializer


class UserRegistrationView(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.filter(username=username).first()

        if not user or not user.is_active:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('The password is incorrect!')

        token = RefreshToken.for_user(user)
        update_last_login(None, user)

        return Response({'id': user.id, 'user': user.username,
                         'access': str(token.access_token), 'refresh': str(token)})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response("Successful Logout", status.HTTP_200_OK)
        except Exception as err:
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikeView(APIView):
    queryset = Like.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=request.data['post_id'])
        like = self.queryset.filter(author=request.user, post=post.id).first()
        if like:
            return Response('You have already liked this post.')
        serializer = LikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        post = Post.objects.get(id=request.data['post_id'])
        like = self.queryset.filter(author=request.user, post=post.id).first()
        if not like:
            return Response('You did not like this post.')

        like.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class LikeAnalytic(APIView):
    def get(self, request, *args, **kwargs):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        queryset = Like.objects.filter(date_created__gte=date_from, date_created__lte=date_to) \
            .values('date_created').annotate(amount=Count('id'))
        serializer = LikeAmountSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class UserActivity(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserActivitySerializer
    authentication_classes = [JWTAuthentication]
