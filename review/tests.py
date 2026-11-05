from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Review
from accounts.models import User
from books.models import Book, Author, Genre

# Create your tests here.
class ReviewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='deeja', first_name='Khadija', last_name ="Ismail", email='khadijaismail@gmail.com')
        self.client.force_authenticate(user=self.user)
        self.author = Author.objects.create(name='Sala Marshal', bio="Born during the war in Iran which inspires her to think about how her people suffered and wanted to write a story about that.", country='Iran')
        self.genre = Genre.objects.create(name="Science Fiction", description="Stories about science.")
        self.book =  Book.objects.create(title='New Book another', description='This is a new book', isbn='5432', publication_date='2026-09-08', genre=self.genre, author=self.author)
        self.book1 = Book.objects.create(title='New Book', description='This is a new book', isbn='7890', publication_date='2026-09-08', genre=self.genre, author=self.author)

        # self.review = Review.objects.create(user=self.user, book=self.book1, rating=3, comment="I really loved it")
    def test_create_review(self):
        review_data = {
            "rating" : 3,
            "comment" : "I really loved it"
        }
        response = self.client.post(reverse(f"create_list_review", args=[self.book1.id]), data=review_data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message']['rating'], 3)

    def test_create_review_error(self):
        response = self.client.post(reverse("create_list_review", args=[3456]), data={"rating" : 3}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_review_rating(self):
        response = self.client.post(reverse("create_list_review", args=[self.book.id]), data={"rating" : 6, "comment" : "I Love it"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_review(self):
        response = self.client.get(reverse("create_list_review", args=[self.book1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_review(self):

        Review.objects.create(user=self.user, book=self.book, rating=3, comment='I love it')
        Review.objects.create(user=self.user, book=self.book, rating=4, comment='I love it')

        response = self.client.get(reverse("get_my_review"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Review.objects.all()), 2)

    def test_update_review(self):
        response = self.client.patch(reverse("edit_delete_review", args=[self.book1.id]), data={"rating" : 4}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

