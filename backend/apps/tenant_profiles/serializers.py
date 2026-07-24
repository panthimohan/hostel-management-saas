from rest_framework import serializers

from django.contrib.auth import get_user_model

from apps.accounts.serializers import UserSerializer
from apps.accounts.models import Role

from apps.beds.models import BedAllocation

from .models import TenantProfile


User = get_user_model()



class CreateTenantSerializer(serializers.ModelSerializer):
    """
    Creates:
    - Tenant User account
    - Tenant Profile
    - Automatically assigns organization
    """

    email = serializers.EmailField(
        write_only=True
    )

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )


    first_name = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True
    )


    last_name = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True
    )


    phone = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True
    )


    class Meta:

        model = TenantProfile

        fields = (

            "email",
            "password",

            "first_name",
            "last_name",
            "phone",

            "photo",

            "emergency_contact_name",
            "emergency_contact_phone",

            "address",

            "identification_type",
            "identification_number",

            "identification_document_front",
            "identification_document_back",

            "university",
            "student_id",
            "course",

        )



    def validate_email(self,value):

        if User.objects.filter(
            email__iexact=value
        ).exists():

            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return value



    def create(self, validated_data):

        request = self.context["request"]


        email = validated_data.pop(
            "email"
        )

        password = validated_data.pop(
            "password"
        )


        first_name = validated_data.pop(
            "first_name",
            ""
        )

        last_name = validated_data.pop(
            "last_name",
            ""
        )

        phone = validated_data.pop(
            "phone",
            ""
        )



        user = User.objects.create_user(

            email=email,

            password=password,

            first_name=first_name,

            last_name=last_name,

            phone=phone,

            role=Role.TENANT,

            organization=request.user.organization

        )



        profile = TenantProfile.objects.create(

            user=user,

            organization=request.user.organization,

            **validated_data

        )


        return profile






class TenantProfileSerializer(serializers.ModelSerializer):


    user_detail = UserSerializer(
        source="user",
        read_only=True
    )


    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )


    first_name = serializers.CharField(
        source="user.first_name",
        read_only=True
    )


    last_name = serializers.CharField(
        source="user.last_name",
        read_only=True
    )


    phone = serializers.CharField(
        source="user.phone",
        read_only=True
    )


    current_allocation = serializers.SerializerMethodField()



    class Meta:

        model = TenantProfile


        fields = (

            "id",

            "user",

            "user_detail",

            "email",

            "first_name",

            "last_name",

            "phone",


            "photo",


            "emergency_contact_name",

            "emergency_contact_phone",


            "address",


            "identification_type",

            "identification_number",


            "identification_document_front",

            "identification_document_back",


            "university",

            "student_id",

            "course",


            "current_allocation",


            "organization",


            "created_at",

            "updated_at",

        )


        read_only_fields = (

            "id",

            "organization",

            "created_at",

            "updated_at",

            "email",

            "first_name",

            "last_name",

            "phone",

        )



    def update(self, instance, validated_data):

        user_data = validated_data.pop(
            "user",
            {}
        )


        user = instance.user


        for attr, value in user_data.items():

            setattr(
                user,
                attr,
                value
            )


        user.save()



        for attr, value in validated_data.items():

            setattr(
                instance,
                attr,
                value
            )


        instance.save()


        return instance




    def get_current_allocation(self,obj):


        allocation = (
            BedAllocation.objects
            .select_related(
                "bed",
                "bed__room",
                "bed__room__hostel",
            )
            .filter(
                tenant=obj.user,
                check_out_date__isnull=True
            )
            .first()
        )


        if not allocation:

            return None



        return {

            "allocation_id":
                allocation.id,


            "bed_id":
                allocation.bed.id,


            "room_id":
                allocation.bed.room.id,


            "hostel_id":
                allocation.bed.room.hostel.id,


            "hostel":
                allocation.bed.room.hostel.name,


            "room_number":
                allocation.bed.room.room_number,


            "bed_number":
                allocation.bed.bed_number,


            "check_in_date":
                allocation.check_in_date,

        }



    def validate_user(self,user):

        request = self.context["request"]


        if user.role != Role.TENANT:

            raise serializers.ValidationError(
                "Only tenant users can have profiles."
            )


        if (
            not request.user.is_superuser
            and request.user.role != "SUPER_ADMIN"
            and user.organization_id != request.user.organization_id
        ):

            raise serializers.ValidationError(
                "Tenant belongs to another organization."
            )


        return user