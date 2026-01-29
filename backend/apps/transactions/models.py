from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class Category(models.Model):

    TRANSACTION_TYPES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="category")
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    icon = models.CharField(max_length=50, default="📁")
    color = models.CharField(max_length=7, default="#3B82F6")
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Category"
        ordering = ["name"]
        unique_together = ["user", "name", "type"]

    def __str__(self):
        return f"{self.name} ({self.type})"


class Transaction(models.Model):

    TRANSACTION_TYPE = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="transactions"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    description = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        indexes = [
            models.Index(fields=["user", "date"]),
            models.Index(fields=["user", "type"]),
            models.Index(fields=["user", "category"]),
        ]

    def __str__(self):
        return f"{self.type} : {self.amount} - {self.date}"
