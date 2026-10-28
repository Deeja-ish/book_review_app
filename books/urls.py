from django.urls import path, include
from .views import GenreListCreateAPIView, GenreUpdateDeteleAPIView, AuthorListCreateView, AuthorUpdateDeleteView, BookListCreatAPIView, BookUpdateDeleteAPIView

urlpatterns = [
    path("genre_create_list/", GenreListCreateAPIView.as_view(), name="genre_create_list"),
    path("genre_delete_update/<int:id>/", GenreUpdateDeteleAPIView.as_view(), name="genre_delete_update"),
    path("author_create_list/", AuthorListCreateView.as_view(), name="author_create_list"),
    path("author_delete_update/<int:id>/", AuthorUpdateDeleteView.as_view(), name="author_update_delete"),
    path("book_create_list/", BookListCreatAPIView.as_view(), name="book_create_list"),
    path("book_delete_update/<int:id>/", BookUpdateDeleteAPIView.as_view(), name="book_delete_update")
]