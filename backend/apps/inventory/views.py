from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from permissions.roles import BelongsToSameOrganization, IsHostelOwnerOrManager, OrganizationIsActive

from .models import InventoryItem
from .serializers import InventoryItemSerializer


class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    permission_classes = [
        IsAuthenticated, IsHostelOwnerOrManager, OrganizationIsActive, BelongsToSameOrganization,
    ]
    filterset_fields = ["hostel", "category", "condition"]

    def get_queryset(self):
        user = self.request.user
        qs = InventoryItem.objects.select_related("hostel").all()
        if user.is_superuser or user.role == "SUPER_ADMIN":
            org_id = self.request.query_params.get("organization")
            return qs.filter(organization_id=org_id) if org_id else qs
        return qs.filter(organization_id=user.organization_id)

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)
