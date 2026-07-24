from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from permissions.roles import BelongsToSameOrganization, IsHostelOwnerOrManager, OrganizationIsActive

from .models import StaffMember
from .serializers import StaffMemberSerializer


class StaffMemberViewSet(viewsets.ModelViewSet):
    serializer_class = StaffMemberSerializer
    permission_classes = [
        IsAuthenticated, IsHostelOwnerOrManager, OrganizationIsActive, BelongsToSameOrganization,
    ]
    filterset_fields = ["hostel", "position", "status"]

    def get_queryset(self):
        user = self.request.user
        qs = StaffMember.objects.select_related("hostel", "user").all()
        if user.is_superuser or user.role == "SUPER_ADMIN":
            org_id = self.request.query_params.get("organization")
            return qs.filter(organization_id=org_id) if org_id else qs
        return qs.filter(organization_id=user.organization_id)

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)
