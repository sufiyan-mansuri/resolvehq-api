from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.tickets.models import Ticket
from apps.notifications.models import Notification

@receiver(post_save, sender=Ticket)
def create_assignment_notification(sender, instance, created, update_fields, **kwargs):
    if not created:
        if update_fields and 'assigned_to' in update_fields:
            if instance.assigned_to:
                message = f"You have been assigned ticket #{instance.id}"

                Notification.objects.create(
                    user=instance.assigned_to,
                    ticket=instance,
                    message=message
                )

@receiver(post_save, sender=Ticket)
def ticket_status_notifier(sender, instance, created, update_fields, **kwargs):
    if created:
        return
    
    if update_fields and 'status' in update_fields:
        if instance.status == Ticket.StatusChoices.IN_PROGRESS:
            if 'assigned_to' in update_fields and instance.assigned_to:
                Notification.objects.create(
                    user=instance.assigned_to,
                    ticket=instance,
                    message=f"You have been assigned ticket #{instance.id}"
                )
        elif instance.status == Ticket.StatusChoices.RESOLVED:
            Notification.objects.create(
                user=instance.created_by,
                ticket=instance,
                message=f"Your ticket #{instance.id} has been resolved"
            )
        elif instance.status == Ticket.StatusChoices.CLOSED:
            Notification.objects.create(
                user=instance.created_by,  
                ticket=instance,
                message=f"Your ticket #{instance.id} has been closed"
            )


