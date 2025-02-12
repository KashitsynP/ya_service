from django.contrib.auth import authenticate
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, RetrieveAPIView, \
    GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from .serializers import (
    SignupSerializer,
    SignInSerializer,
    UserInfoSerializer,
    LogoutSerializer, LatencySerializer,
)


class SignUpView(CreateAPIView):
    """User registration and issuance of access/refresh tokens."""

    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generating tokens
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "User registered successfully",
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            },
            status=status.HTTP_201_CREATED
        )


class SignInView(APIView):
    """User authorization and issuance of access/refresh tokens."""

    serializer_class = SignInSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        id = serializer.validated_data["id"]
        password = serializer.validated_data["password"]

        user = authenticate(request, id=id, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generating tokens
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            },
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    """User logout with option to delete all tokens."""

    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data.get("refresh")
        all_tokens = serializer.validated_data.get("all", False)

        try:
            if all_tokens:
                # Clearing all active user sessions (if we stored them in the database)
                # BlacklistedToken.objects.filter(user=request.user).delete()
                pass
            else:
                # Adding a refresh token to the blacklist
                token = RefreshToken(refresh_token)
                token.blacklist()

            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

        except Exception:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(RetrieveAPIView):
    """Getting information about the current user."""

    serializer_class = UserInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LatencyView(GenericAPIView):
    """Returns the delay from the service to ya.ru."""

    serializer_class = LatencySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            response = requests.get("https://ya.ru")
            return Response({'latency': response.elapsed.total_seconds()})
        except requests.RequestException:
            return Response(
                {"error": "Failed to reach ya.ru"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
