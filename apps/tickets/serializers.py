from rest_framework import serializers
from apps.tickets.models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "title", "description", "status", "priority", "organization", "created_by", "assigned_to", "created_at"]
        read_only_fields = ["id", "status", "priority", "organization", "created_by", "assigned_to", "created_at"]

class StaffTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "title", "description", "status", "priority", "organization", "created_by", "assigned_to", "created_at"]
        read_only_fields = ["id", "status", "organization",  "created_by", "created_at"]