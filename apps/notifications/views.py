from rest_framework import generics
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from rest_framework.views import APIView
from apps.organizations.models import Membership
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    get=extend_schema(
        summary="Get user notifications",
        description="Returns a list of all notifications for the currently authenticated user.",
        tags=['Notifications']
    )
)
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        )

@extend_schema_view(
    patch=extend_schema(
        summary="Toggle read status",
        description="Marks a specific notification as read or unread by passing `{'is_read': true}`.",
        tags=['Notifications']
    )
)
class NotificationUpdateView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch', 'options']

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


