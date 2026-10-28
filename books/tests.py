from django.test import TestCase
from django.urls import reverse
from rest_framework import status 
from .models import Genre, Author, Book
from rest_framework.test import APIClient

# Create your tests here.

data = {
    "name" : "Mystery",
    "description" : "Stories About Science that have a little bit touch of impossible realities."
}
update = {
    "name" : "Tragedy"
}
# creating the genre test case
class GenreAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.genre = Genre.objects.create(name="Science Fiction", description="Stories about science.")

    # create a test for creating genre
    def test_genre_create_view(self):
        response = self.client.post(reverse("genre_create_list"), data=data,  format='json')
        print("Response Data :", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # create a test for listing genre  
    def test_genre_list_view(self):
        response = self.client.get(reverse("genre_create_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['message']), 1)

    def test_genre_fetch(self):
        response = self.client.get(reverse("genre_delete_update", args=[self.genre.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message']["name"], "Science Fiction")

    def test_genre_bad_request(self):
        self.client.post(reverse("genre_create_list"), data=data, format='json')
        response = self.client.post(reverse("genre_create_list"), data=data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_genre_update(self):
        resposne = self.client.patch(reverse("genre_delete_update", args=[self.genre.id]), data=update, format='json')
        self.assertEqual(resposne.status_code, status.HTTP_200_OK)
        self.assertNotEqual(resposne.data['message']['name'], "Science Fiction")

    def test_genre_delete(self):
        resposne = self.client.delete(reverse("genre_delete_update", args=[self.genre.id]))
        self.assertEqual(resposne.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Genre.objects.filter(id=self.genre.id).exists())


