from django.contrib import admin

# Register your models here.
from .models import Book, Author, Genre

# creatr a custom admin for the book model 
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "isbn", "author", "genre", "publication_date")
    search_fields = ("title", 'author', 'genre', "isbn")
    list_filter = ("genre", 'author')


# create a custom admin for the author model 
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "bio", "country")
    search_fields = ("country",)

# create a custom admin for the genre model 
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    