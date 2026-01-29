from django.urls import path
from . import views

app_name = "analytics"

urlpatterns = [
    path("dashboard/", views.dashboard_stats, name="dashboard_stats"),
    path(
        "expenses-by-category", views.expenses_by_category, name="expenses_by_category"
    ),
    path("spending-trend", views.spending_trend, name="spending_trend"),
    path("budget-progress/", views.budget_progress, name="budget_process"),
]
