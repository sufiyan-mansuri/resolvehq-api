from rest_framework import serializers
from .models import Comment
from apps.organizations.models import Membership
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.first_name", default="System User", read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(source="author", read_only=True)
    author_role = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            "id",
            "body",
            "is_internal",
            "created_at",
            'author_id',
            'author_name', 
            'author_role'
        ]
        read_only_fields = ['id', 'created_at']

    @extend_schema_field(OpenApiTypes.STR)
    def get_author_role(self, obj):
        if not obj.author:
            return 'Unknown'
            
        try:
            membership = Membership.objects.get(
                user=obj.author, 
                organization=obj.ticket.organization
            )
            return membership.role
            
        except Membership.DoesNotExist:
            return 'Unknown'