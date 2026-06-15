from rest_framework import serializers
from apps.users.models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "first_name", "last_name", "role"]

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    tokens = serializers.JSONField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        
        return {
            'email': user.email,
            'tokens': user.tokens,
        }
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')