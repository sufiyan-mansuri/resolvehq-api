from django.urls import path
from .views import CustomTokenRefreshView
from apps.users.views import RegisterAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name="token_refresh"),
]
