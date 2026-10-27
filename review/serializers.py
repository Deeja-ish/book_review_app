from rest_framework import serializers
from .models import Review

# create the review serializer
class ReviewSerializer(serializers.ModelSerilizer):
    class Meta:
        model = Review
        fields = ["id", "user", "book", "rating", "comment", "created_at"]