from django.shortcuts import render
from rest_framework.views import APIView
from .models import Author, Book, Genre
from .serializers import AuthorSerializer, BookSerializer, GenreSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Avg, Count
from common.pagination import CustomPagePaginator
# from django.core.exceptions import ObjectDoesNotExist

# creating the genre views
class GenreListCreateAPIView(APIView):
    # create the list request
    def get(self, request):
        list_genre = Genre.objects.all()
        serilaizer = GenreSerializer(list_genre, many=True)
        return Response({"status" : "success", "message" : serilaizer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = GenreSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status" : "success", "message" : serializer.data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class GenreUpdateDeteleAPIView(APIView):
    def get(self, request, id):
        try: 
            get_genre = Genre.objects.get(id=id)
        except Genre.DoesNotExist:
            return Response({"status" : "error", "message" : "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GenreSerializer(get_genre)
        return Response({"status" : "success", "message": serializer.data}, status=status.HTTP_200_OK)
    # create a view to update a 
    def patch(self, request, id):
        try:
            update_genre = Genre.objects.get(id=id)
        except Genre.DoesNotExist:
            return Response({"status" : "error", "message" : "Genre Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GenreSerializer(update_genre, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"success", "message" :  serializer.data}, status=status.HTTP_200_OK)
        return Response({"message" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # create the delete
    def delete(self, request, id):
        try:
            delete_genre = Genre.objects.get(id=id)
        except Genre.DoesNotExist:
            return Response({"status" : "error", "message" : "Not found"}, status=status.HTTP_404_NOT_FOUND)
        delete_genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# creating the author view
class AuthorListCreateView(APIView):
    def get(self, request):
        list_author = Author.objects.all()
        serializer = AuthorSerializer(list_author, many=True)
        return Response({"status" : "success", "message" : serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = AuthorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status" : "success", "message" : serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status" : "error", "message" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class AuthorUpdateDeleteView(APIView):
    def get(self, request, id):
        list_author = Author.objects.get(id=id)
        serailizer = AuthorSerializer(list_author)
        return Response({"status" : "success", "message" : serailizer.data}, status=status.HTTP_200_OK)

    def patch(self, request, id):
        try:
            get_author = Author.objects.get(id=id)
        except Author.DoesNotExist:
            return Response({"status" : "error", "message" : "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorSerializer(get_author, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status" : "success", "message" : serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        try:
            delete_author = Author.objects.get(id=id)
        except Author.DoesNotExist():
            return Response({"status" : "error", "message" : "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        delete_author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Creating the book views 
class BookListCreatAPIView(APIView):
    def get(self, request):
        book_list = Book.objects.select_related("author", "genre").all().annotate(
            review_count=Count("review_book"),
            average_rating = Avg("review_book__rating")
        )

        # search by filter 
        search = request.query_params.get("search")
        if search:
            book_list = book_list.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(author__name__icontains=search) |
                Q(genre__name__icontains=search)
            )

        # search by ordering 
        # create a function for ordering the books by title, author genre and data 
        allowed_ordering_fields = ["title", "author__name", "genre__name", "publication_date"]
        ordering = request.query_params.get("ordering")
        if ordering in allowed_ordering_fields:
            book_list = book_list.order_by(ordering)

        # add pagination
        pagination = CustomPagePaginator()
        page = pagination.paginate_queryset(book_list, request)
        serializer = BookSerializer(page, many=True)
        return pagination.get_paginated_response({"status" : "success", "message" : serializer.data})

    def post(self, request):
        data = request.data
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status" : "success", "message" : serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status" : "error", "message" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BookUpdateDeleteAPIView(APIView):
    def patch(self, request, id):
        try:
            update_book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response({"status" : "error", "message" : "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(update_book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status" : "success", "message" : serializer.data}, status=status.HTTP_200_OK)
        return Response({"status" : "success", "message" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # delete a book 
    def delete(self, request, id):
        try:
            delete_book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response({"status" : "error", "message" : "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        delete_book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        