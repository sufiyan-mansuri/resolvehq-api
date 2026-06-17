from django.db import models
from apps.common.models import BaseModel
from apps.users.models import CustomUser
from django.utils.text import slugify
from apps.common.utils import generate_random_string
from django.utils import timezone
import secrets

class Organization(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="organizations")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.name)}-{generate_random_string()}"
        super().save(*args, **kwargs)

class Membership(BaseModel):
    class RoleChoices(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        AGENT = 'agent', 'Agent'
        CUSTOMER = 'customer', 'Customer'

    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACTIVE = 'active', 'Active'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="memberships")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=RoleChoices.choices, default=RoleChoices.CUSTOMER)
    status = models.CharField(max_length=8, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    token = models.CharField(max_length=64, unique=True, null=True, blank=True)
    token_expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'organization'],
                name='unique_user_organization_membership'
            )
        ]

    def generate_invite_token(self, hours_valid=24):
        self.token = secrets.token_urlsafe(32)
        self.token_expires_at = timezone.now() + timezone.timedelta(hours=hours_valid)
        self.status = self.StatusChoices.PENDING