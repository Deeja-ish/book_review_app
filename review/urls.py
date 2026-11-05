from .views import ReviewCreateListView, ReviewDetailView, ReviewMyListView
from django.urls import path

urlpatterns = [
    path("book/<int:book_id>/review/", ReviewCreateListView.as_view(), name="create_list_review"),
    path("review/<int:id>/", ReviewDetailView.as_view(), name="edit_delete_review"),
    path("list_review/", ReviewMyListView.as_view(), name="get_my_review")
]