from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from permissions.roles import BelongsToSameOrganization, IsFrontDeskStaff, OrganizationIsActive

from .models import Visitor
from .serializers import VisitorSerializer


class VisitorViewSet(viewsets.ModelViewSet):
    serializer_class = VisitorSerializer
    permission_classes = [
        IsAuthenticated, IsFrontDeskStaff, OrganizationIsActive, BelongsToSameOrganization,
    ]
    filterset_fields = ["hostel", "tenant_visited"]

    def get_queryset(self):
        user = self.request.user
        qs = Visitor.objects.select_related("tenant_visited", "hostel").all()
        if user.is_superuser or user.role == "SUPER_ADMIN":
            org_id = self.request.query_params.get("organization")
            return qs.filter(organization_id=org_id) if org_id else qs
        return qs.filter(organization_id=user.organization_id)

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization, logged_by=self.request.user)

    @action(detail=True, methods=["post"])
    def check_out(self, request, pk=None):
        visitor = self.get_object()
        visitor.exit_time = timezone.now()
        visitor.save(update_fields=["exit_time", "updated_at"])
        return Response(self.get_serializer(visitor).data)
