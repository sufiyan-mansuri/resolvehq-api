from rest_framework import viewsets
from apps.tickets.serializers import TicketSerializer, StaffTicketSerializer
from rest_framework.permissions import IsAuthenticated
from apps.common.utils import get_current_org
from .models import Ticket
from apps.organizations.models import Membership, Organization
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        tenant_data = get_current_org(self.request, self.kwargs)
        membership = tenant_data['membership']

        if membership.role == Membership.RoleChoices.CUSTOMER:
            return Ticket.objects.filter(organization=tenant_data['organization'], created_by=self.request.user)

        return Ticket.objects.filter(organization=tenant_data['organization'])

    def perform_create(self, serializer):
        with transaction.atomic():
            organization = get_object_or_404(Organization, slug=self.kwargs.get('slug'))

            Membership.objects.get_or_create(
                user=self.request.user,
                organization=organization,
                defaults= {
                    'role': Membership.RoleChoices.CUSTOMER,
                    'status': Membership.StatusChoices.ACTIVE
                }
            )

            serializer.save(
                created_by = self.request.user,
                organization = organization
            )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        ticket = self.get_object()

        tenant_data = get_current_org(request, self.kwargs)
        membership = tenant_data['membership']
        print(membership)
        if membership.role == Membership.RoleChoices.CUSTOMER:
            if ticket.status != Ticket.StatusChoices.OPEN:
                raise PermissionDenied("Customers can only edit tickets that are currently Open.")

            serializer = TicketSerializer(ticket, data=request.data, partial=partial)
        else:
            serializer = StaffTicketSerializer(ticket, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        get_current_org(request, self.kwargs, Membership.RoleChoices.ADMIN)

        return super().destroy(request, *args, **kwargs)