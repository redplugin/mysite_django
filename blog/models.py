from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models


class NewPostManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(created_at__gt=datetime.now()-timedelta(hours=24))


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.pk})"


class Post(models.Model):

    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    new_posts = NewPostManager()
    objects = models.Manager()

    def __str__(self):
        return f"{self.title} ({self.pk})"

    class Meta:
        db_table = 'posts'
        ordering = ['title']
        unique_together = ('title', 'content')
        indexes = [
            models.Index(fields=['title', 'content']),  # compound indexes
        ]
        default_related_name = 'posts'


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content} ({self.pk})"


class TestUser(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField(default=18)


    def __str__(self):
        return f"{self.name}"

