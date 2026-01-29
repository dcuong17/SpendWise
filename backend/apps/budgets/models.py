from django.db import models
from django.contrib.auth import get_user_model
from apps.transactions.models import Category

User = get_user_model()

# Create your models here.


class Budget(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="budgets"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.DateField(help_text="First day of the month")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-month"]
        unique_together = ["user", "category", "month"]
        indexes = [
            models.Index(fields=["user", "month"]),
        ]

    def __str__(self):
        return f"{self.category.name} - {self.month.strftime('%B %Y')} : {self.amount}"
