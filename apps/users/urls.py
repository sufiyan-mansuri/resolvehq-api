from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from apps.users.views import RegisterAPIView, LoginAPIView, LogoutAPIView, ProtectedTestAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('protected/', ProtectedTestAPIView.as_view(), name="protected"),
]
