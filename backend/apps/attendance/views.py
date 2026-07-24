from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from permissions.roles import BelongsToSameOrganization, IsFrontDeskStaff, OrganizationIsActive

from .models import AttendanceRecord
from .serializers import AttendanceRecordSerializer


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceRecordSerializer
    permission_classes = [
        IsAuthenticated, IsFrontDeskStaff, OrganizationIsActive, BelongsToSameOrganization,
    ]
    filterset_fields = ["hostel", "tenant", "status", "date"]

    def get_queryset(self):
        user = self.request.user
        qs = AttendanceRecord.objects.select_related("tenant", "hostel").all()
        if user.is_superuser or user.role == "SUPER_ADMIN":
            org_id = self.request.query_params.get("organization")
            return qs.filter(organization_id=org_id) if org_id else qs
        return qs.filter(organization_id=user.organization_id)

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization, marked_by=self.request.user)
