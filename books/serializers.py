from rest_framework import serializers
from .models import Author, Book, Genre

# create the authur serializer
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "bio", "country", "created_at"]

# create the book serializer
class BookSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True, allow_null=True)
    class Meta:
        model = Book
        fields = ["id", "title", "description", "cover_image", "isbn", "publication_date", "author", "genre", "review_count", "average_rating", "created_at"]

# create a genre model 
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name", "description"]

    

