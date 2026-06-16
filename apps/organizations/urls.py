from django.urls import path
from apps.organizations.views import OrganizationListCreateView, OrganizationInviteView, OrganizationInviteAcceptView

urlpatterns = [
    path('', OrganizationListCreateView.as_view()),
    path('<slug:slug>/invite/', OrganizationInviteView.as_view()),
    path('<slug:slug>/accept-invite/', OrganizationInviteAcceptView.as_view()),
]
