from django.db import models
from apps.common.models import BaseModel
from apps.organizations.models import Organization
from apps.users.models import CustomUser

class Ticket(BaseModel):
    class StatusChoices(models.TextChoices):
        OPEN = 'open', 'Open'
        IN_PROGRESS = 'progress', 'In Progress'
        RESOLVED = 'resolved', 'Resolved'
        CLOSED = 'closed', 'Closed'

    class PriorityChoices(models.TextChoices):
        HIGH = 'high', 'High'
        MEDIUM = 'medium', 'Medium'
        LOW = 'low', 'Low'

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.OPEN, db_index=True)
    priority = models.CharField(max_length=10, choices=PriorityChoices.choices, null=True, blank=True, db_index=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="tickets")
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_tickets")
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="assigned_tickets")

    def __str__(self):
        return f"{self.title} - {self.status}"

