from rest_framework import generics
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from rest_framework.views import APIView
from apps.organizations.models import Membership

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        )
    
class NotificationUpdateView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


