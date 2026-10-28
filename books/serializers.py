from rest_framework import serializers
from .models import Author, Book, Genre

# create the authur serializer
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "bio", "country", "created_at"]

# create the book serializer
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "description", "cover_image", "isbn", "publication_date", "author", "genre", "created_at"]

# create a genre model 
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name", "description"]

    

