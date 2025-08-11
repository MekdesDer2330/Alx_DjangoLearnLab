from django.db import models
from django.utils import timezone

# Author model for author entity with one to may relationship(foreignkey in book model)
class Author(models.Model):
    name = models.CharField(max_length=100) 

    def __str__(self):
        return self.name


# Book model-> Each Book is linked to exactly one Author (ForeignKey).
class Book(models.Model):
    title = models.CharField(max_length=200) 
    publication_year = models.IntegerField()  
    author = models.ForeignKey(
        Author,
        related_name='books',  
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
