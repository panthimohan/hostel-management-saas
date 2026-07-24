from datetime import date, timedelta

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from permissions.roles import (
    BelongsToSameOrganization,
    IsHostelOwnerOrManager,
    IsTenantUser,
    OrganizationIsActive,
)

from apps.payments.models import RentInvoice

from .models import Bed, BedAllocation
from .serializers import (
    BedAllocationSerializer,
    BedSerializer,
)



class BedViewSet(viewsets.ModelViewSet):

    serializer_class = BedSerializer


    permission_classes = [
        IsAuthenticated,
        IsHostelOwnerOrManager,
        OrganizationIsActive,
        BelongsToSameOrganization,
    ]


    filterset_fields = [
        "room",
        "status",
    ]



    def get_queryset(self):

        user = self.request.user


        qs = (
            Bed.objects
            .select_related(
                "room",
                "room__hostel"
            )
            .order_by(
                "room",
                "bed_number"
            )
        )



        if user.is_superuser or user.role == "SUPER_ADMIN":

            org_id = self.request.query_params.get(
                "organization"
            )


            if org_id:

                return qs.filter(
                    organization_id=org_id
                )


            return qs



        return qs.filter(
            organization_id=user.organization_id
        )




    def perform_create(self, serializer):

        bed = serializer.save(
            organization=self.request.user.organization
        )


        bed.status = "VACANT"

        bed.save()





class MyAllocationView(APIView):

    """
    Tenant current and previous room allocations.
    """


    permission_classes = [
        IsAuthenticated,
        IsTenantUser,
    ]



    def get(self, request):

        allocations = (
            BedAllocation.objects
            .select_related(
                "bed",
                "bed__room",
                "bed__room__hostel"
            )
            .filter(
                tenant=request.user
            )
            .order_by(
                "-check_in_date"
            )
        )



        current = (
            allocations
            .filter(
                check_out_date__isnull=True
            )
            .first()
        )



        def serialize(allocation):

            room = allocation.bed.room


            return {

                "id":
                    allocation.id,


                "hostel_name":
                    room.hostel.name,


                "room_number":
                    room.room_number,


                "bed_number":
                    allocation.bed.bed_number,


                "room_type":
                    room.room_type,


                "price":
                    str(room.price),


                "check_in_date":
                    allocation.check_in_date,


                "check_out_date":
                    allocation.check_out_date,

            }




        return Response({

            "current":
                serialize(current)
                if current
                else None,


            "history":
                [
                    serialize(a)
                    for a in allocations
                    if a.check_out_date
                ]

        })







class BedAllocationViewSet(viewsets.ModelViewSet):


    serializer_class = BedAllocationSerializer



    permission_classes = [

        IsAuthenticated,

        IsHostelOwnerOrManager,

        OrganizationIsActive,

        BelongsToSameOrganization,

    ]



    filterset_fields = [

        "bed",

        "tenant",

    ]





    def get_queryset(self):

        user = self.request.user



        qs = (

            BedAllocation.objects

            .select_related(

                "bed",

                "bed__room",

                "tenant"

            )

            .order_by(

                "-check_in_date"

            )

        )





        if user.is_superuser or user.role == "SUPER_ADMIN":


            org_id = self.request.query_params.get(
                "organization"
            )


            if org_id:

                return qs.filter(
                    organization_id=org_id
                )


            return qs





        return qs.filter(

            organization_id=user.organization_id

        )







    def perform_create(self, serializer):


        allocation = serializer.save(

            organization=self.request.user.organization

        )



        bed = allocation.bed



        # Occupy bed

        bed.status = "OCCUPIED"

        bed.save()





        # ----------------------------
        # Create first rent invoice
        # ----------------------------


        room = bed.room



        billing_start = (

            allocation.check_in_date

            if allocation.check_in_date

            else date.today()

        )



        billing_end = (

            billing_start.replace(day=28)

            + timedelta(days=4)

        ).replace(day=1) - timedelta(days=1)





        RentInvoice.objects.create(

            organization=self.request.user.organization,


            bed_allocation=allocation,


            billing_period_start=billing_start,


            billing_period_end=billing_end,


            due_date=billing_start + timedelta(days=7),


            rent_amount=room.price,


            security_deposit=0,


            utility_amount=0,


            late_fee=0,

        )







    def perform_update(self, serializer):


        allocation = serializer.save()



        if allocation.check_out_date:


            bed = allocation.bed



            bed.status = "VACANT"



            bed.save()