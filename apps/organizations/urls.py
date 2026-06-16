from django.urls import path
from apps.organizations.views import OrganizationListCreateView

urlpatterns = [
    path('', OrganizationListCreateView.as_view()),
]
