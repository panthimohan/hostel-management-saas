from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from permissions.roles import BelongsToSameOrganization, IsFrontDeskStaff, OrganizationIsActive

from .models import Reservation, ReservationStatus
from .serializers import ReservationSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [
        IsAuthenticated, IsFrontDeskStaff, OrganizationIsActive, BelongsToSameOrganization,
    ]
    filterset_fields = ["hostel", "status", "room"]

    def get_queryset(self):
        user = self.request.user
        qs = Reservation.objects.select_related("hostel", "room").all()
        if user.is_superuser or user.role == "SUPER_ADMIN":
            org_id = self.request.query_params.get("organization")
            return qs.filter(organization_id=org_id) if org_id else qs
        return qs.filter(organization_id=user.organization_id)

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization, created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        reservation = self.get_object()
        reservation.status = ReservationStatus.CONFIRMED
        reservation.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(reservation).data)

    @action(detail=True, methods=["post"])
    def waitlist(self, request, pk=None):
        reservation = self.get_object()
        reservation.status = ReservationStatus.WAITLISTED
        reservation.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(reservation).data)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        reservation.status = ReservationStatus.CANCELLED
        reservation.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(reservation).data)
