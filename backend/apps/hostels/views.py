from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from permissions.roles import BelongsToSameOrganization, IsHostelOwnerOrManager, OrganizationIsActive

from .models import Hostel
from .serializers import HostelSerializer


class HostelViewSet(viewsets.ModelViewSet):
    """
    CRUD for hostel locations, strictly scoped to the requesting
    user's organization. Super Admins may pass ?organization=<id>
    to view a specific tenant's hostels. Locked until the org is
    approved (status=ACTIVE) by a Super Admin.
    """

    serializer_class = HostelSerializer
    permission_classes = [
        IsAuthenticated, IsHostelOwnerOrManager, OrganizationIsActive, BelongsToSameOrganization,
    ]
    filterset_fields = ["city", "country"]

    def get_queryset(self):
        user = self.request.user
        qs = Hostel.objects.all().order_by("-created_at")
        if user.is_superuser or user.role == "SUPER_ADMIN":
            org_id = self.request.query_params.get("organization")
            return qs.filter(organization_id=org_id) if org_id else qs
        return qs.filter(organization_id=user.organization_id)

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)
