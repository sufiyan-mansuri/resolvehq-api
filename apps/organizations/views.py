from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from apps.organizations.models import Organization, Membership
from apps.organizations.serializers import OrganizationSerializer
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.users.models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from apps.common.utils import get_current_org
from django.utils import timezone
from django.shortcuts import get_object_or_404

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
                role=Membership.RoleChoices.ADMIN,
                status=Membership.StatusChoices.ACTIVE,
            )

class OrganizationInviteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        tenant_data = get_current_org(request, self.kwargs, required_role=Membership.RoleChoices.ADMIN)
        organization = tenant_data["organization"]

        email = request.data.get('email')
        if not email:
            return Response({'detail': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.filter(email=email).first()
        if not user: 
            return Response(
                {'detail': 'No user found with this email. Ask them to register first.'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        existing_membership = Membership.objects.filter(user=user, organization=organization).first()

        if existing_membership:
            if existing_membership.status == Membership.StatusChoices.ACTIVE:
                return Response(
                    {'detail': 'This user is already an active member of the organization.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            existing_membership.generate_invite_token()
            existing_membership.save()

            return Response(
                {'token': existing_membership.token, 'detail': 'Invite resent successfully.'}, 
                status=status.HTTP_200_OK
            )
        
        new_membership = Membership(
            user=user,
            organization=organization, 
            role=Membership.RoleChoices.AGENT
        )

        new_membership.generate_invite_token()
        new_membership.save()

        return Response(
            {'token': new_membership.token, 'detail': 'Invite sent successfully.'}, 
            status=status.HTTP_201_CREATED
        )

class OrganizationInviteAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        
        invite_token = request.data.get('token')
        if not invite_token:
            return Response({'detail': 'Invite Token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        membership = get_object_or_404(
            Membership, 
            token=invite_token,
            organization__slug=slug,
            user=request.user,
            status=Membership.StatusChoices.PENDING,
        )
        
        if membership.token_expires_at < timezone.now():
            return Response(
                {"detail": "This token has expired. Please ask the Admin to resend your invite."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        membership.status = Membership.StatusChoices.ACTIVE
        membership.token = None
        membership.token_expires_at = None
        membership.save()

        

        return Response({"detail": "Invite accepted. Welcome to the organization!"}, status=status.HTTP_200_OK)
        

        

