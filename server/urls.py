from server.apps import ServerConfig
from django.urls import path
from . import views
from .views import IndexView, start_mailing_view, RecipientListView, RecipientCreateView, RecipientUpdateView, \
    RecipientDetailView, RecipientDeleteView, MessageListView, MessageCreateView, MessageUpdateView, MessageDetailView, \
    MessageDeleteView, MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView

app_name = ServerConfig.name



urlpatterns = [
    path('recipient/create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipient/view/', RecipientListView.as_view(), name='recipient_list'),
    path('recipient/<int:pk>/update/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/<int:pk>/detail/',RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipient/<int:pk>/delete/', RecipientDeleteView.as_view(), name='recipient_confirm_delete'),
    path('message/view/', MessageListView.as_view(), name='message_list'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/detail/',MessageDetailView.as_view(), name='message_detail'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_confirm_delete'),
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('', IndexView.as_view(), name='index'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_confirm_delete'),
]

