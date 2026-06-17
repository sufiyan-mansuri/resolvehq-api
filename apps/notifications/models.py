from django.db import models
from apps.common.models import BaseModel
from apps.users.models import CustomUser
from apps.tickets.models import Ticket

class Notification(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications")
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    
