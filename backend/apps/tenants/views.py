import logging

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from permissions.roles import IsSuperAdmin

from .models import Organization, OrganizationStatus
from .serializers import OrganizationSerializer

logger = logging.getLogger("apps.tenants")
User = get_user_model()


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    Super Admin only: view and manage every hostel business on the
    platform, including approving/rejecting new signups and
    suspending/reactivating existing ones.
    """

    queryset = Organization.objects.all().order_by("-created_at")
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    filterset_fields = ["status", "subscription_plan"]

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        organization = self.get_object()
        organization.status = OrganizationStatus.ACTIVE
        organization.save(update_fields=["status", "updated_at"])
        logger.info("Organization %s approved by user_id=%s", organization.id, request.user.id)
        return Response(OrganizationSerializer(organization).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        organization = self.get_object()
        organization.status = OrganizationStatus.CANCELLED
        organization.save(update_fields=["status", "updated_at"])
        logger.info("Organization %s rejected by user_id=%s", organization.id, request.user.id)
        return Response(OrganizationSerializer(organization).data)

    @action(detail=True, methods=["post"])
    def suspend(self, request, pk=None):
        organization = self.get_object()
        organization.status = OrganizationStatus.SUSPENDED
        organization.save(update_fields=["status", "updated_at"])
        logger.warning("Organization %s suspended by user_id=%s", organization.id, request.user.id)
        return Response(OrganizationSerializer(organization).data)

    @action(detail=True, methods=["post"])
    def reactivate(self, request, pk=None):
        organization = self.get_object()
        organization.status = OrganizationStatus.ACTIVE
        organization.save(update_fields=["status", "updated_at"])
        logger.info("Organization %s reactivated by user_id=%s", organization.id, request.user.id)
        return Response(OrganizationSerializer(organization).data)
