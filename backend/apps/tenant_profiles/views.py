from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from permissions.roles import (
    BelongsToSameOrganization,
    IsHostelOwnerOrManager,
    IsFrontDeskStaff,
    OrganizationIsActive,
)

from apps.beds.models import BedAllocation

from .models import TenantProfile
from .serializers import (
    TenantProfileSerializer,
    CreateTenantSerializer,
)


class TenantProfileViewSet(viewsets.ModelViewSet):
    """
    Tenant management.

    Owner/Manager/Receptionist can create tenant accounts.
    Owner/Manager can manage tenant profiles.
    Tenants can access their own profile through /me/.
    """

    serializer_class = TenantProfileSerializer
    filterset_fields = ["user"]


    def get_serializer_class(self):

        if self.action == "create":
            return CreateTenantSerializer

        return TenantProfileSerializer



    def get_permissions(self):

        if self.action == "me":
            return [
                IsAuthenticated()
            ]


        if self.action == "create":
            return [
                IsAuthenticated(),
                IsHostelOwnerOrManager(),
                OrganizationIsActive(),
            ]


        return [
            IsAuthenticated(),
            IsFrontDeskStaff(),
            OrganizationIsActive(),
            BelongsToSameOrganization(),
        ]



    def get_queryset(self):

        user = self.request.user

        queryset = TenantProfile.objects.select_related(
            "user"
        ).all()


        if user.is_superuser or user.role == "SUPER_ADMIN":

            organization_id = self.request.query_params.get(
                "organization"
            )

            if organization_id:
                return queryset.filter(
                    organization_id=organization_id
                )

            return queryset



        return queryset.filter(
            organization_id=user.organization_id
        )



    def perform_create(self, serializer):

        serializer.save()



    def destroy(self, request, *args, **kwargs):

        tenant_profile = self.get_object()

        tenant_user = tenant_profile.user


        # Close active bed allocation before deleting tenant
        active_allocations = BedAllocation.objects.filter(
            tenant=tenant_user,
            check_out_date__isnull=True
        )


        today = timezone.now().date()


        for allocation in active_allocations:

            allocation.check_out_date = today
            allocation.save()


            bed = allocation.bed

            # Check if bed has any other active tenant
            still_occupied = BedAllocation.objects.filter(
                bed=bed,
                check_out_date__isnull=True
            ).exists()


            if not still_occupied:

                bed.status = "VACANT"
                bed.save()



        # delete tenant profile
        tenant_profile.delete()


        return Response(
            status=status.HTTP_204_NO_CONTENT
        )



    @action(
        detail=False,
        methods=["post"],
        url_path="create-tenant"
    )
    def create_tenant(self, request):

        serializer = CreateTenantSerializer(
            data=request.data,
            context={
                "request": request
            }
        )


        serializer.is_valid(
            raise_exception=True
        )


        tenant_profile = serializer.save()


        return Response(
            TenantProfileSerializer(
                tenant_profile
            ).data,
            status=status.HTTP_201_CREATED
        )



    @action(
        detail=False,
        methods=["get", "patch"]
    )
    def me(self, request):

        profile, created = TenantProfile.objects.get_or_create(
            user=request.user,
            defaults={
                "organization": request.user.organization
            }
        )


        if request.method == "PATCH":

            serializer = self.get_serializer(
                profile,
                data=request.data,
                partial=True
            )


            serializer.is_valid(
                raise_exception=True
            )


            serializer.save()


            return Response(
                serializer.data
            )


        return Response(
            self.get_serializer(profile).data
        )