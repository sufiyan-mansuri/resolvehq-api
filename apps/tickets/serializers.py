from rest_framework import serializers
from apps.tickets.models import Ticket
from apps.organizations.models import Membership
from drf_spectacular.utils import extend_schema_field
from apps.comments.serializers import CommentSerializer

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

class TicketDetailSerializer(serializers.ModelSerializer):
    comment_timeline = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'status', 'priority', 'assigned_to', 'created_by', 'created_at', 'updated_at', 'comment_timeline']
    
    @extend_schema_field(CommentSerializer(many=True))
    def get_comment_timeline(self, obj):
        request = self.context.get('request')
        if not request:
            return []

        comments = obj.comments.all()

        try:
            membership = Membership.objects.get(
                user=request.user,
                organization=obj.organization
            )
            
            if membership.role == Membership.RoleChoices.CUSTOMER:
                comments = comments.filter(is_internal=False)
                
        except Membership.DoesNotExist:
            return []

        serializer = CommentSerializer(comments, many=True, context=self.context)
        return serializer.data