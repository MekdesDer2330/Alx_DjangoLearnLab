from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book

# Book Serializer-> Serializes all Book fields and includes custom validation
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """Ensure publication year is not in the future."""
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# Author Serializer-> Serializes author name and includes nested books.
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  
    # 'books' comes from the related_name in Book.author

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
