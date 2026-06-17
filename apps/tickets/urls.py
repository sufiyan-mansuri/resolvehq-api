from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.tickets.views import TicketViewSet

ticket_list_create = TicketViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

ticket_detail = TicketViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('<slug:slug>/', ticket_list_create, name="ticket-list"),
    path('<slug:slug>/<uuid:pk>/', ticket_detail, name="ticket-detail")
]
