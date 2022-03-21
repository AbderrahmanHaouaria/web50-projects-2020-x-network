from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', blank=True, symmetrical=False)
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="followed_by")

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=512)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User)