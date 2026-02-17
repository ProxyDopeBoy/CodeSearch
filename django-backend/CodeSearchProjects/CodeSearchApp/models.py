from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ProfilePage(models.Model):
    username = models.CharField(max_length = 50)
    avatar = models.ImageField(upload_to='media/user_avatar')
    aboutme = models.TextField(blank=True)
    age = models.IntegerField(default=0, blank=True)
    last_activity = models.DateTimeField(default=timezone.now)

def __str__(self):
    return self.username


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=85)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='media/post_image', blank=True)
    stack = models.CharField(max_length=40, default='python')
    saved_by = models.ManyToManyField(User, related_name='saved_posts', blank=True)

class Code(models.Model):
    post = models.ForeignKey(Post, related_name='code_examples', on_delete=models.CASCADE)
    code = models.TextField()


def __str__(self):
    return self.author

