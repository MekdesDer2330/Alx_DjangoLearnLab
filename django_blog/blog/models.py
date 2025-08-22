# blog/models.py
from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug  = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager(blank=True)  # ← tagging

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title