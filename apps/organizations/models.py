from django.db import models
from apps.common.models import BaseModel
from apps.users.models import CustomUser
from django.utils.text import slugify
from apps.common.utils import generate_random_string

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

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="memberships")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=RoleChoices.choices, default=RoleChoices.CUSTOMER)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'organization'],
                name='unique_user_organization_membership'
            )
        ]