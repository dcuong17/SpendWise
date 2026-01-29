from rest_framework import serializers
from .models import Budget


class BudgetSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(source="category.name", read_only=True)
    category_icon = serializers.CharField(source="category.icon", read_only=True)
    category_color = serializers.CharField(source="category.color", read_only=True)

    class Meta:
        model = Budget
        fields = [
            "id",
            "category",
            "category_name",
            "category_icon",
            "category_color",
            "amount",
            "month",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
