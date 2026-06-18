from rest_framework import generics, status, permissions
from rest_framework.response import Response
from apps.users.serializers import RegisterSerializer, LoginSerializer, LogoutSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import TokenRefreshView

@extend_schema_view(
    post=extend_schema(
        summary="Register a new user",
        description="Creates a new account and returns the user details.",
        auth=[],
        tags=['Users']
    )
)
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="User Login",
        description="Authenticates a user using email and password, returning JWT access and refresh tokens.",
        auth=[],
        tags=['Users']
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="User Logout",
        description="Blacklists the provided refresh token so it can no longer be used.",
        tags=['Users']
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomTokenRefreshView(TokenRefreshView):
    @extend_schema(
        summary="Refresh JWT Token",
        description="Takes a valid refresh token in the payload and returns a new access token.",
        auth=[],
        tags=['Users'] 
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)