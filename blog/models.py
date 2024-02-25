from django.db import models
from django.contrib.auth.models import User

from django.db.models import CheckConstraint
from django.db.models import Q


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.pk})"


class Post(models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField()
    categories = models.ManyToManyField(Category, related_name="posts")  # linked to CATEGORIES
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.pk})"

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(title__startswith='Hello'),  # Ensure the title starts with "Hello"
                name='post_title_must_start_with_hello'  # Give the constraint a descriptive name
            )
        ]


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content} ({self.pk})"

