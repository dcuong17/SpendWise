from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from apps.transactions.models import Transaction
from apps.budgets.models import Budget


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics for current month."""
    user = request.user
    today = timezone.now().date()
    first_day = today.replace(day=1)

    month_transactions = Transaction.objects.filter(
        user=user, date__gte=first_day, date__lte=today
    )

    income = (
        month_transactions.filter(type="income").aggregate(total=Sum("amount"))["total"]
        or 0
    )
    expenses = (
        month_transactions.filter(type="expense").aggregate(total=Sum("amount"))[
            "total"
        ]
        or 0
    )
    balance = income - expenses
    transaction_count = month_transactions.count()

    return Response(
        {
            "income": float(income),
            "expenses": float(expenses),
            "balance": float(balance),
            "transaction_count": transaction_count,
            "month": first_day.strftime("%B %Y"),
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def expenses_by_category(request):
    """Get expenses grouped by category for pie chart."""
    user = request.user
    today = timezone.now().date()
    first_day = today.replace(day=1)

    category_expenses = (
        Transaction.objects.filter(
            user=user, type="expense", date__gte=first_day, date__lte=today
        )
        .values("category__name", "category__color", "category__icon")
        .annotate(total=Sum("amount"), count=Count("id"))
        .order_by("-total")
    )

    return Response(list(category_expenses))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def spending_trend(request):
    """Get daily spending for last 30 days."""
    user = request.user
    today = timezone.now().date()
    start_date = today - timedelta(days=30)

    daily_expenses = (
        Transaction.objects.filter(
            user=user, type="expense", date__gte=start_date, date__lte=today
        )
        .values("date")
        .annotate(total=Sum("amount"))
        .order_by("date")
    )

    return Response(list(daily_expenses))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def budget_progress(request):
    """Get budget vs actual spending."""
    user = request.user
    today = timezone.now().date()
    first_day = today.replace(day=1)

    budgets = Budget.objects.filter(user=user, month=first_day).select_related(
        "category"
    )

    result = []
    for budget in budgets:
        spent = (
            Transaction.objects.filter(
                user=user,
                category=budget.category,
                type="expense",
                date__gte=first_day,
                date__lte=today,
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

        percentage = (spent / budget.amount * 100) if budget.amount > 0 else 0

        result.append(
            {
                "category": budget.category.name,
                "category_icon": budget.category.icon,
                "category_color": budget.category.color,
                "budget": float(budget.amount),
                "spent": float(spent),
                "remaining": float(budget.amount - spent),
                "percentage": round(percentage, 2),
            }
        )

    return Response(result)
