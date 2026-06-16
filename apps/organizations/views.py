from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from apps.organizations.models import Organization, Membership
from apps.organizations.serializers import OrganizationSerializer
from django.db import transaction
from rest_framework.permissions import IsAuthenticated

class OrganizationListCreateView(ListCreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Organization.objects.filter(
            membership__user=self.request.user
        )

    def perform_create(self, serializer):

        with transaction.atomic():
            organization = serializer.save(owner=self.request.user)

            Membership.objects.create(
                user=self.request.user,
                organization=organization, 
                role=Membership.RoleChoices.ADMIN
            )