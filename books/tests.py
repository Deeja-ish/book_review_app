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

author_data = {
    "name" : "Umme",
    "bio" : "Born is Sudan. had lead a life of peace and properity until the start of the war that tore her family apart which inspire her to start writing stories about the peacefull era.",
    "country" : "Sudan"
}

update_author = {
    "country" : "Palastine"
}

class AuthorAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author1 = Author.objects.create(name='Sala Marshal', bio="Born during the war in Iran which inspires her to think about how her people suffered and wanted to write a story about that.", country='Iran')
        self.author2 = Author.objects.create(name="Daniel Master", bio='Loved poetry and history and with a passion for untold stories', country='Kenya')

    def test_author_fetch(self):
        response = self.client.get(reverse("author_create_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(len(response.data['message']), 2)

    def test_author_create(self):
        response = self.client.post(reverse("author_create_list"), data=author_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"]['name'], "Umme")

    def test_update_author(self):
        response = self.client.patch(reverse("author_delete_update", args=[self.author1.id]), data=update_author, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['message']["country"], "Iran")
        self.assertEqual(response.data['message']['country'], "Palastine")

    def test_author_bad_request(self):
        response = self.client.post(reverse("author_create_list"), data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(response.data)

    def test_author_delete(self):
        response = self.client.delete(reverse("author_delete_update", args=[self.author2.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class BookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.genre = Genre.objects.create(name="Mystery", description='Suspense Stories')
        self.author = Author.objects.create(name='Khadija Ismail', bio="Born in Nigeria and has a passion for story writing.", country="Nigeria")
        self.book = Book.objects.create(title="Oliver Twist", description="The story about an orphan boy", isbn="RN2356", publication_date="2026-01-01", author=self.author, genre=self.genre)
        self.author1 = Author.objects.create(name="Sadiq Goni", bio = "A story writer in kano", country='Nigeria')
        self.genre1 = Genre.objects.create(name="Adventures", description='travel Adventures')
        self.book1 = Book.objects.create(title="The Adventures of Tom Sawyer", description="A story about a very naughty boy", isbn="RN7865", publication_date="2026-01-01", author=self.author1, genre=self.genre1)
        self.new_data = {
            "title" : "The Adventure of Khadija",
            "description" : "The Story of a girl on her journey to discover",
            "isbn" : "RN7654",
            "publication_date" : "2026-02-02",
            "author" : self.author.id,
            "genre" : self.genre.id
        }
        self.update = {
            "title" : "Oliver Twist First Edition"
        }

    def test_book_get(self):
        response = self.client.get(reverse("book_create_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Book.objects.all()), 2)

    def test_book_create(self):
        response = self.client.post(reverse("book_create_list"), data=self.new_data, format="json")
        self.assertIn("message", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message']['title'], "The Adventure of Khadija")

    def test_book_bad_request(self):
        response = self.client.post(reverse("book_create_list"), data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_update(self):
        response = self.client.patch(reverse("book_delete_update", args=[self.book.id]), data=self.update, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['message']['title'], "Oliver Twist")
    
    # test book_update with unknow id 
    def test_book_update_unknow_id(self):
        response = self.client.patch(reverse("book_delete_update", args=["676544"]), data=self.update, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test the title
    def test_search_title(self):
        response = self.client.get(reverse("book_create_list"), {"search" : "Adventure"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(response.data['results']["message"][0]['title'], "The Adventures of Tom Sawyer")

    # test description
    def test_search_description(self):
        response = self.client.get(reverse("book_create_list"), {"search" : "Adventures"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(response.data['results']['message']), 0)

    # test author
    def test_search_author(self):
        response = self.client.get(reverse("book_create_list"), {"search" : self.author.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Book.objects.filter(author=self.author).exists())
    
    # test genre
    def test_search_genre(self):
        response = self.client.get(reverse("book_create_list"), {"search": self.genre.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Book.objects.filter(genre=self.genre).exists())

    # test the ordering 
    def test_book_ordering(self):
        response = self.client.get(reverse("book_create_list"), {"ordering" : "title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book = response.data['results']['message']
        self.assertEqual(book[0]['title'], "Oliver Twist")

    # test book pagination 
    def test_book_pagination(self):
        response = self.client.get(reverse("book_create_list"), {"page" : 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)

    # test pagination 
    def test_book_pagination_limit(self):
        for i in range(1, 12):
            Book.objects.create(title=f"Book Title {i}", description=f"Book description {i}", isbn=f"ISBN:{i}", publication_date="2026-01-01", author=self.author, genre=self.genre)
        response = self.client.get(reverse("book_create_list"), {'page' : 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data['results']['message']), 1)

        # create another response 
        response_second_page = self.client.get(reverse("book_create_list"), {"page" : 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']['message']), 1)