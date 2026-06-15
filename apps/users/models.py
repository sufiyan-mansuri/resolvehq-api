from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(
            email = self.normalize_email(email),
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("role", CustomUser.RoleChoices.ADMIN)

        user = self.create_user(
            email,
            password=password,
            **extra_fields,
        )
        
        return user

class CustomUser(AbstractBaseUser):
    class RoleChoices(models.TextChoices):
        ADMIN = 'Admin'
        AGENT = 'Agent'
        CUSTOMER = 'Customer'

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=RoleChoices.choices, default=RoleChoices.CUSTOMER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    class Meta:
        verbose_name = "User"