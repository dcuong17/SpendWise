from django.urls import path, include
from .views import CategoryViewSet, TransactionViewSet
from rest_framework.routers import DefaultRouter

app_name = "transactions"

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"", TransactionViewSet, basename="transaction")

urlpatterns = [path("", include(router.urls))]
