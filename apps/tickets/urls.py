from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.tickets.views import TicketViewSet
from apps.comments.views import CommentListCreateView

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

ticket_assign = TicketViewSet.as_view({
    'post': 'assign'
})

ticket_resolve = TicketViewSet.as_view({
    'post': 'resolve'
})

ticket_close = TicketViewSet.as_view({
    'post': 'close'
})

urlpatterns = [
    path('<slug:slug>/', ticket_list_create, name="ticket-list"),
    path('<slug:slug>/<uuid:pk>/', ticket_detail, name="ticket-detail"),
    path('<slug:slug>/<uuid:pk>/assign/', ticket_assign, name='ticket-assign'),
    path('<slug:slug>/<uuid:pk>/resolve/', ticket_resolve, name='ticket-resolve'),
    path('<slug:slug>/<uuid:pk>/close/', ticket_close, name='ticket-close'),
    path('<slug:slug>/<uuid:ticket_id>/comments/', CommentListCreateView.as_view(), name='ticket-comments'),
]
