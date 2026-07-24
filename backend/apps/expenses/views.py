from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from permissions.roles import BelongsToSameOrganization, IsAccountingStaff, OrganizationIsActive

from .models import Expense, Income
from .serializers import ExpenseSerializer, IncomeSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [
        IsAuthenticated, IsAccountingStaff, OrganizationIsActive, BelongsToSameOrganization,
    ]
    filterset_fields = ["hostel", "category", "payment_method"]

    def get_queryset(self):
        user = self.request.user
        qs = Expense.objects.select_related("hostel").all()
        if user.is_superuser or user.role == "SUPER_ADMIN":
            org_id = self.request.query_params.get("organization")
            return qs.filter(organization_id=org_id) if org_id else qs
        return qs.filter(organization_id=user.organization_id)

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization, recorded_by=self.request.user)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        """
        Category breakdown + total, for dashboard charts.
        Optional query params: ?hostel=<id>&from=YYYY-MM-DD&to=YYYY-MM-DD
        """
        qs = self.filter_queryset(self.get_queryset())
        date_from = request.query_params.get("from")
        date_to = request.query_params.get("to")
        if date_from:
            qs = qs.filter(incurred_on__gte=date_from)
        if date_to:
            qs = qs.filter(incurred_on__lte=date_to)

        by_category = (
            qs.values("category")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )
        grand_total = qs.aggregate(total=Sum("amount"))["total"] or 0

        return Response({
            "total": grand_total,
            "by_category": [
                {
                    "category": row["category"],
                    "category_display": dict(Expense._meta.get_field("category").choices)[row["category"]],
                    "total": row["total"],
                }
                for row in by_category
            ],
        })


class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [
        IsAuthenticated, IsAccountingStaff, OrganizationIsActive, BelongsToSameOrganization,
    ]
    filterset_fields = ["hostel", "payment_method"]

    def get_queryset(self):
        user = self.request.user
        qs = Income.objects.select_related("hostel").all()
        if user.is_superuser or user.role == "SUPER_ADMIN":
            org_id = self.request.query_params.get("organization")
            return qs.filter(organization_id=org_id) if org_id else qs
        return qs.filter(organization_id=user.organization_id)

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization, recorded_by=self.request.user)
