from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=200, blank=True,
                            help_text='Comma-separated tags (e.g. travel,python)')
    likes = models.ManyToManyField(
        User, related_name='liked_posts', through='Like', blank=True)
    views = models.PositiveIntegerField(default=0)
    bookmarked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='bookmarks',
        blank=True
    )

    def get_tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    @property
    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    blog = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.blog.title}"


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    blog = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name='blog_likes')  # ✅ Rename here
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'blog')

    def __str__(self):
        return f"{self.user.username} likes {self.blog.title}"
