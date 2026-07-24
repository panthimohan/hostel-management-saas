from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.tenants.models import Organization, OrganizationStatus

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = (
            "id",
            "email",
            "phone",
            "first_name",
            "last_name",
            "role",
            "organization",
            "two_factor_enabled",
            "date_joined",
        )


class RegisterSerializer(serializers.ModelSerializer):
    """
    Public user registration.

    Creates TENANT accounts only.
    Hostel owners are created through OwnerSignupSerializer.
    Staff accounts are created by owners/admins.
    """

    password = serializers.CharField(
        write_only=True,
        min_length=10
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone",
            "password",
        )

        read_only_fields = (
            "id",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            email=validated_data["email"],
            phone=validated_data.get("phone", ""),
            password=password,
            role="TENANT",
        )

        return user


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Login serializer.

    Adds role and organization information to JWT.
    Returns user details after successful authentication.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["role"] = user.role
        token["organization_id"] = user.organization_id

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = UserSerializer(self.user).data

        return data


class OwnerSignupSerializer(serializers.Serializer):
    """
    Creates a new hostel organization and its first HOSTEL_OWNER user.
    """

    organization_name = serializers.CharField(
        max_length=255
    )

    email = serializers.EmailField()

    phone = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True
    )

    password = serializers.CharField(
        write_only=True,
        min_length=10
    )


    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return value


    def validate_organization_name(self, value):
        if Organization.objects.filter(
            name__iexact=value
        ).exists():

            raise serializers.ValidationError(
                "An organization with this name already exists."
            )

        return value


    @transaction.atomic
    def create(self, validated_data):

        organization = Organization.objects.create(
            name=validated_data["organization_name"],
            status=OrganizationStatus.PENDING,
        )


        owner = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            phone=validated_data.get("phone", ""),
            role="HOSTEL_OWNER",
            organization=organization,
        )


        organization.owner = owner

        organization.save(
            update_fields=["owner"]
        )


        return organization


    def to_representation(self, instance):

        return {
            "organization_id": instance.id,
            "organization_name": instance.name,
            "status": instance.status,
            "detail": (
                "Your hostel business has been registered and is pending "
                "Super Admin approval. You can log in now, but hostel "
                "management features unlock after approval."
            ),
        }


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()



class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()

    token = serializers.CharField()

    new_password = serializers.CharField(
        write_only=True,
        min_length=10
    )