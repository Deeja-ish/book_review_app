from django.shortcuts import render
from rest_framework.views import APIView
from .models import Author, Book, Genre
from .serializers import AuthorSerializer, BookSerializer, GenreSerializer
from rest_framework.response import Response
from rest_framework import status 
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
            return Response({"status" : "error", "message" : "Not found"})
        serializer = GenreSerializer(get_genre)
        return Response({"status" : "success", "message": serializer.data}, status=status.HTTP_200_OK)
    # create a view to update a 
    def patch(self, request, id):
        try:
            update_genre = Genre.objects.get(id=id)
        except Genre.DoesNotExist:
            return Response({"status" : "error", "message" : "Genre Not Found"})
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
            return Response({"status" : "error", "message" : "Not found"})
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
            return Response({"status" : "error", "message" : "Not Found"})
        serializer = AuthorSerializer(get_author, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status" : "success", "message" : serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        try:
            delete_author = Author.objects.get(id=id)
        except Author.DoesNotExist():
            return Response({"status" : "error", "message" : "Not Found"})
        delete_author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Creating the book views 
class BookListCreatAPIView(APIView):
    def get(self, request):
        book_list = Book.objects.select_related("author", "genre").all()
        serializer = BookSerializer(book_list, many=True)
        return Response({"status" : "success", "message" :serializer.data}, status=status.HTTP_200_OK)

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
            return Response({"status" : "error", "message" : "Not Found"})
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
            return Response({"status" : "error", "message" : "Not Found"})
        delete_book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)