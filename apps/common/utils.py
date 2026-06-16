import string
import random
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

def generate_random_string(length=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choices(chars, k=length))

def get_current_org(request, view_kwargs, required_role=None):
    from apps.organizations.models import Organization, Membership

    slug = view_kwargs.get('slug')
    
    if not slug: 
        PermissionDenied('Organization slug is missing.')

    organization = get_object_or_404(Organization, slug=slug)

    query_params = {
        'user': request.user,
        'organization': organization,
        'status': Membership.StatusChoices.ACTIVE
    }

    if required_role:
        query_params['role'] = required_role

    membership = Membership.objects.filter(**query_params).first()

    if not membership:
        raise PermissionDenied("You do not have the required permissions for this organization.")
    
    return {
        "organization": organization,
        "membership": membership
    }
