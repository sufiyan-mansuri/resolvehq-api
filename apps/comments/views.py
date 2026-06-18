from rest_framework.generics import ListCreateAPIView
from .serializers import CommentSerializer
from apps.common.utils import get_current_org
from django.shortcuts import get_object_or_404
from apps.tickets.models import Ticket
from .models import Comment
from apps.organizations.models import Membership
from rest_framework.exceptions import PermissionDenied

class CommentListCreatView(ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_ticket_and_check_permissions(self):
        tenant_data = get_current_org(self.request, self.kwargs)
        membership = tenant_data['membership']

        ticket = get_object_or_404(
            Ticket,
            id=self.kwargs['ticket_id'],
            organization = tenant_data['organization']
        )

        if membership.role == Membership.RoleChoices.CUSTOMER:
            if ticket.created_by != self.request.user:
                raise PermissionDenied("You can only access comments on your own tickets.")
        elif membership.role == Membership.RoleChoices.AGENT:
            if ticket.assigned_to != self.request.user:
                raise PermissionDenied("You can only access comments on tickets assigned to you.")
            
        return ticket, membership
    
    def get_queryset(self):
        ticket, membership = self.get_ticket_and_check_permissions()

        queryset = Comment.objects.filter(ticket=ticket)

        if membership.role == Membership.RoleChoices.CUSTOMER:
            queryset = queryset.filter(is_internal=False)

        return queryset
    
    def perform_create(self, serializer):
        ticket, membership = self.get_ticket_and_check_permissions()

        is_internal = self.request.data.get('is_internal', False)

        if membership.role == Membership.RoleChoices.CUSTOMER:
            is_internal = False

        serializer.save(
            author=self.request.user, 
            ticket=ticket,
            is_internal=is_internal
        )