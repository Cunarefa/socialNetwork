from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    last_activity = models.DateTimeField(blank=True, null=True)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField(max_length=1000, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField(User, related_name='liked_posts')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like')
    date_created = models.DateField(auto_now_add=True)








