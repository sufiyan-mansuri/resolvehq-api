from rest_framework import viewsets, status
from apps.tickets.serializers import TicketSerializer, StaffTicketSerializer
from rest_framework.permissions import IsAuthenticated
from apps.common.utils import get_current_org
from .models import Ticket
from apps.organizations.models import Membership, Organization
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

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
    
    @action(detail=True, methods=['post'])
    def assign(self, request, slug=None, pk=None):
        tenant_data = get_current_org(request, self.kwargs, Membership.RoleChoices.ADMIN)

        ticket = self.get_object()

        target_agent_id = request.data.get('agent')
        if not target_agent_id:
            return Response({'detail': 'Agent ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        target_agent_membership = Membership.objects.filter(
            user__id=target_agent_id,
            organization=tenant_data['organization'],
            role__in=[Membership.RoleChoices.ADMIN, Membership.RoleChoices.AGENT],
            status=Membership.StatusChoices.ACTIVE
        ).first()

        if not target_agent_membership:
            return Response(
                {'detail': 'The specified user is not an active agent in this organization.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        valid_states = [Ticket.StatusChoices.OPEN, Ticket.StatusChoices.IN_PROGRESS]
        if ticket.status not in valid_states:
            return Response(
                {'detail': f'Cannot assign a ticket that is currently marked as {ticket.status}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_new_assignee = ticket.assigned_to != target_agent_membership.user

        ticket.assigned_to = target_agent_membership.user
        ticket.status = Ticket.StatusChoices.IN_PROGRESS

        fields_to_save = ['status']

        if is_new_assignee:
            fields_to_save.append('assigned_to')

        ticket.save(update_fields=fields_to_save)

        return Response(
            {'detail': f'Ticket assigned to {target_agent_membership.user.email} and moved to In Progress.'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, slug=None, pk=None):
        tenant_data = get_current_org(request, self.kwargs)
        membership = tenant_data['membership']

        ticket = self.get_object()

        if membership.role == Membership.RoleChoices.CUSTOMER:
            raise PermissionDenied("Customers are not permitted to resolve tickets.")

        if membership.role == Membership.RoleChoices.AGENT:
            if ticket.assigned_to != request.user:
                raise PermissionDenied("You can only resolve tickets that are directly assigned to you.")

        if ticket.status != Ticket.StatusChoices.IN_PROGRESS:
            return Response(
                {'detail': f'Cannot resolve a ticket that is currently marked as {ticket.status}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        ticket.status = Ticket.StatusChoices.RESOLVED

        ticket.save(update_fields=['status'])

        return Response(
            {'detail': f'Ticket #{ticket.id} resolved successfully.'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def close(self, request, slug=None, pk=None):
        tenant_data = get_current_org(request, self.kwargs, Membership.RoleChoices.ADMIN)

        ticket = self.get_object()

        if ticket.status != Ticket.StatusChoices.RESOLVED:
            return Response(
                {'detail': f'Cannot close a ticket that is currently marked as {ticket.status}.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ticket.status = Ticket.StatusChoices.CLOSED
        ticket.save(update_fields=['status'])

        return Response(
            {'detail': f'Ticket #{ticket.id} closed successfully.'},
            status=status.HTTP_200_OK
        )