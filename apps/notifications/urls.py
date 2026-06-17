from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name="notification-list"),
    path('<uuid:pk>/read/', views.NotificationUpdateView.as_view(), name="notification-update"),
]
