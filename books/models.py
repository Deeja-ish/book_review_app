from django.db import models

# Create your models here.
# create the author model 
class Author(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField(max_length=500, blank=True)
    country = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # add meta to order by name
    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"

# create the genre model
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # add meta to order by name
    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.description}"

# create the book model 
class Book(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=1000, blank=True)
    cover_image = models.ImageField(blank=True)
    isbn = models.CharField(max_length=50, unique=True)
    publication_date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='book_author')
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name='book_genre')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} - {self.isbn}"


