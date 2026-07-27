import logging

import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import (
    urlsafe_base64_decode,
    urlsafe_base64_encode,
)

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


from permissions.roles import (
    IsHostelOwnerOrManager,
    OrganizationIsActive,
)


from .serializers import (
    EmailTokenObtainPairSerializer,
    OwnerSignupSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    UserSerializer,
)


logger = logging.getLogger("apps.accounts")


User = get_user_model()


LOCKOUT_THRESHOLD = 5

LOCKOUT_DURATION_MINUTES = 15




class LoginView(TokenObtainPairView):

    """
    Email + password login.
    Tracks failed attempts and locks accounts.
    """


    serializer_class = EmailTokenObtainPairSerializer

    throttle_scope = "auth"



    def post(self, request, *args, **kwargs):

        email = request.data.get("email")


        user = User.objects.filter(
            email=email
        ).first()



        if user and user.is_locked:

            return Response(
                {
                    "detail":
                    "Account temporarily locked due to repeated failed logins."
                },
                status=status.HTTP_423_LOCKED,
            )



        response = super().post(
            request,
            *args,
            **kwargs
        )



        if user:


            if response.status_code == 200:


                user.failed_login_attempts = 0

                user.locked_until = None



                user.save(
                    update_fields=[
                        "failed_login_attempts",
                        "locked_until",
                    ]
                )



                logger.info(
                    "Successful login for user_id=%s",
                    user.id
                )



            else:


                user.failed_login_attempts += 1



                if user.failed_login_attempts >= LOCKOUT_THRESHOLD:


                    from datetime import timedelta


                    user.locked_until = (
                        timezone.now()
                        +
                        timedelta(
                            minutes=LOCKOUT_DURATION_MINUTES
                        )
                    )



                    logger.warning(
                        "Account locked user_id=%s",
                        user.id
                    )



                user.save(
                    update_fields=[
                        "failed_login_attempts",
                        "locked_until",
                    ]
                )



        return response






class RegisterView(generics.CreateAPIView):


    queryset = User.objects.all()


    serializer_class = RegisterSerializer


    permission_classes = [
        permissions.AllowAny
    ]


    throttle_scope = "auth"






class OwnerSignupView(generics.CreateAPIView):


    """
    Public endpoint for hostel owner registration.
    """


    serializer_class = OwnerSignupSerializer


    permission_classes = [
        permissions.AllowAny
    ]


    throttle_scope = "auth"




    def create(self, request, *args, **kwargs):


        serializer = self.get_serializer(
            data=request.data
        )


        serializer.is_valid(
            raise_exception=True
        )



        organization = serializer.save()



        logger.info(
            "New owner signup organization_id=%s",
            organization.id
        )



        return Response(
            serializer.to_representation(
                organization
            ),
            status=status.HTTP_201_CREATED
        )







class LogoutView(APIView):


    """
    Blacklists refresh token.
    """


    permission_classes = [
        permissions.IsAuthenticated
    ]




    def post(self, request):


        refresh_token = request.data.get(
            "refresh"
        )



        if not refresh_token:


            return Response(
                {
                    "detail":
                    "refresh token required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )



        try:


            token = RefreshToken(
                refresh_token
            )


            token.blacklist()



        except TokenError:


            return Response(
                {
                    "detail":
                    "invalid token"
                },
                status=status.HTTP_400_BAD_REQUEST
            )



        return Response(
            status=status.HTTP_205_RESET_CONTENT
        )







class MeView(generics.RetrieveUpdateAPIView):


    serializer_class = UserSerializer


    permission_classes = [
        permissions.IsAuthenticated
    ]


    http_method_names = [
        "get",
        "patch",
        "head",
        "options",
    ]




    def get_object(self):

        return self.request.user

class PasswordResetRequestView(generics.GenericAPIView):
    """
    Sends password reset link to user's email.
    """

    serializer_class = PasswordResetRequestSerializer

    permission_classes = [
        permissions.AllowAny
    ]

    throttle_scope = "auth"


    def post(self, request):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )


        email = serializer.validated_data["email"]


        user = User.objects.filter(
            email__iexact=email
        ).first()


        response_data = {
            "detail":
            "If an account with that email exists, a reset link has been sent."
        }


        if user:

            uid = urlsafe_base64_encode(
                force_bytes(user.pk)
            )


            token = default_token_generator.make_token(
                user
            )


            reset_url = (
                f"{settings.FRONTEND_URL}/reset-password/"
                f"?uid={uid}&token={token}"
            )


            email_body = f"""
Hello {user.email},

You requested a password reset for your Nestled Hostel account.

Click the link below to reset your password:

{reset_url}

If you did not request this, you can ignore this email.

Regards,
Nestled Hostel
"""


            send_mail(
                subject="Nestled Hostel Password Reset",
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[
                    user.email
                ],
                fail_silently=False,
            )


            logger.info(
                "Password reset email sent to user_id=%s",
                user.id
            )


        return Response(
            response_data,
            status=status.HTTP_200_OK
        )

class PasswordResetConfirmView(generics.GenericAPIView):


    serializer_class = PasswordResetConfirmSerializer


    permission_classes = [
        permissions.AllowAny
    ]


    throttle_scope = "auth"




    def post(self, request):


        serializer = self.get_serializer(
            data=request.data
        )


        serializer.is_valid(
            raise_exception=True
        )



        data = serializer.validated_data




        try:


            uid = force_str(
                urlsafe_base64_decode(
                    data["uid"]
                )
            )



            user = User.objects.get(
                pk=uid
            )



        except (

            User.DoesNotExist,

            ValueError,

            TypeError,

            OverflowError,

        ):


            return Response(

                {
                    "detail":
                    "Invalid reset link."
                },

                status=status.HTTP_400_BAD_REQUEST

            )





        if not default_token_generator.check_token(

            user,

            data["token"]

        ):


            return Response(

                {
                    "detail":
                    "Invalid or expired reset link."
                },

                status=status.HTTP_400_BAD_REQUEST

            )





        user.set_password(

            data["new_password"]

        )



        user.failed_login_attempts = 0

        user.locked_until = None




        user.save(

            update_fields=[

                "password",

                "failed_login_attempts",

                "locked_until",

            ]

        )





        logger.info(

            "Password reset completed for user_id=%s",

            user.id

        )





        return Response(

            {
                "detail":
                "Password has been reset. You can now log in."
            }

        )








class TenantListView(APIView):


    """
    Hostel owners/managers can view tenants
    inside their organization.
    """



    permission_classes = [

        IsAuthenticated,

        IsHostelOwnerOrManager,

        OrganizationIsActive,

    ]





    def get(self, request):


        tenants = User.objects.filter(

            organization=request.user.organization,

            role="TENANT"

        ).values(

            "id",

            "email",

            "phone",

            "date_joined"

        )





        return Response(

            list(tenants)

        )