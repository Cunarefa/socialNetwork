from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator

from .models import User, Post, Like


class UserRegistrationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(max_length=150, required=True,
                                     validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('id', 'username', 'password',)

    def create(self, data):
        user = User(username=data['username'])
        user.set_password(data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(max_length=150, required=True)

    def validate(self, data):
        user = User.objects.filter(username=data.get('username')).first()

        if not user or not user.is_active:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(data['password']):
            raise AuthenticationFailed('The password is incorrect!')

        return user


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(read_only=True, source='author.id')

    class Meta:
        model = Post
        exclude = ('likes',)


class LikeSerializer(serializers.ModelSerializer):
    date_created = serializers.ReadOnlyField()
    author = serializers.ReadOnlyField(read_only=True, source='author.id')
    post = serializers.ReadOnlyField(read_only=True, source='post.id')

    class Meta:
        model = Like
        fields = ('id', 'date_created', 'author', 'post')


class LikeAmountSerializer(serializers.Serializer):
    date_created = serializers.DateField()
    amount = serializers.IntegerField()


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'last_login', 'last_activity',)










