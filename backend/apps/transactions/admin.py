from django.contrib import admin
from .models import Category, Transaction

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "user", "icon", "color"]
    list_filter = ["type"]
    search_fields = ["name", "user__email"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["user", "type", "amount", "category", "date"]
    list_filter = ["type", "category", "date"]
    search_fields = ["user__email", "description"]
    date_hierarchy = "date"
