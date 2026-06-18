from django.db import models
from apps.common.models import BaseModel
from apps.tickets.models import Ticket
from apps.users.models import CustomUser

class Comment(BaseModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name="comments", null=True)
    body = models.TextField()
    is_internal = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        visibility = "Internal" if self.is_internal else "Public"
        return f"Comment by {self.author} on {self.ticket} ({visibility})"
    