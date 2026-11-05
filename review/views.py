from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ReviewCreateSerializer, ReviewSerializer
from rest_framework import status
from .models import Review
from rest_framework.response import Response
from rest_framework import status
from books.models import Book


# Create your views here.
# create the view to get data and post data 
class ReviewCreateListView(APIView):
    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"status" : "error", "message" : "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        review = Review.objects.filter(book=book)
        serializer = ReviewSerializer(review, many=True)
        return Response({"status" : "success", "message" : serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"status" : "error", "message" : "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        serializer = ReviewCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user, book=book)
            return Response({"status" : "success", "message" : serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status" : "error", "message" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# create the view to 
class ReviewDetailView(APIView):
    # view a specific review
    def get(self, request, id):
        try:    
            review = Review.objects.get(id=id, user=request.user)
        except Review.DoesNotExist:
            return Response({"status" : "error", "message" : "Not Found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ReviewSerializer(review)
        return Response({"status" : "success", "message" : serializer.data}, status=status.HTTP_200_OK)

    # update a review
    def patch(self, request, id):
        try:
            review = Review.objects.get(id=id, user=request.user)
        except Review.DoesNotExist:
            return Response({"status" : "error", "message": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewCreateSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status" : "success", "message" : serializer.data}, status=status.HTTP_200_OK)
        return Response({"status" : "error", "message" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # delete a view
    def delete(self, request, id):
        try:
            review = Review.objects.get(id=id, user=request.user)
        except Review.DoesNotExist:
            return Response({"status" : "success", "message": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewMyListView(APIView):
    def get(self, request):
        review = Review.objects.filter(user=request.user)
        serializer = ReviewSerializer(review, many=True)
        return Response({"status" : "success", "message" : serializer.data}, status.HTTP_200_OK)
    