from django.contrib import admin
from .models import Review

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "rating", "comment", "created_at")
    search_fields = ("book__title", "user__username")
    list_filter = ("rating", 'created_at')