from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from permissions.roles import BelongsToSameOrganization, IsHostelOwnerOrManager, OrganizationIsActive

from .models import Room
from .serializers import RoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [
        IsAuthenticated, IsHostelOwnerOrManager, OrganizationIsActive, BelongsToSameOrganization,
    ]
    filterset_fields = ["hostel", "status", "room_type"]

    def get_queryset(self):
        user = self.request.user
        qs = Room.objects.select_related("hostel").order_by("hostel", "room_number")
        if user.is_superuser or user.role == "SUPER_ADMIN":
            org_id = self.request.query_params.get("organization")
            return qs.filter(organization_id=org_id) if org_id else qs
        return qs.filter(organization_id=user.organization_id)

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)
