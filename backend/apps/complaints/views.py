from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from permissions.roles import IsHostelOwnerOrManager, IsTenantUser, OrganizationIsActive

from .models import Complaint, ComplaintStatus
from .serializers import ComplaintSerializer


class ComplaintViewSet(viewsets.ModelViewSet):
    """
    Tenants can create complaints and see only their own.
    Owners/Managers see every complaint for their organization and can
    update status / assign staff.
    """

    serializer_class = ComplaintSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsTenantUser()]
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsHostelOwnerOrManager(), OrganizationIsActive()]

    def get_queryset(self):
        user = self.request.user
        qs = Complaint.objects.select_related("tenant", "hostel").all()
        if user.is_superuser or user.role == "SUPER_ADMIN":
            org_id = self.request.query_params.get("organization")
            return qs.filter(organization_id=org_id) if org_id else qs
        if user.role == "TENANT":
            return qs.filter(tenant=user)
        return qs.filter(organization_id=user.organization_id)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(organization=user.organization, tenant=user)

    @action(detail=True, methods=["post"])
    def start_progress(self, request, pk=None):
        complaint = self.get_object()
        complaint.status = ComplaintStatus.IN_PROGRESS
        complaint.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(complaint).data)

    @action(detail=True, methods=["post"])
    def resolve(self, request, pk=None):
        complaint = self.get_object()
        complaint.status = ComplaintStatus.RESOLVED
        complaint.resolved_at = timezone.now()
        complaint.save(update_fields=["status", "resolved_at", "updated_at"])
        return Response(self.get_serializer(complaint).data)
