from django.db import models
from books.models import Book
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="review_user")
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="review_book")
    rating = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1, message='Rating must be atleast 1'),
        MaxValueValidator(5, message="Rating Cannot be higher that five")

    ])
    comment = models.TextField(max_length=10000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                name='unique_user_book_review'
            )
        ]

    def __str__(self):
        return f"{self.book} - {self.rating} - {self.user__username}"
