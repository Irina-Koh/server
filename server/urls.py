from django.urls import path

from server.apps import ServerConfig

from . import views
from .views import (IndexView, MailingAttemptCreateView,
                    MailingAttemptDeleteView, MailingAttemptDetailView,
                    MailingAttemptListView, MailingAttemptUpdateView,
                    MailingCreateView, MailingDeleteView, MailingDetailView,
                    MailingListView, MailingUpdateView, MessageCreateView,
                    MessageDeleteView, MessageDetailView, MessageListView,
                    MessageUpdateView, RecipientCreateView,
                    RecipientDeleteView, RecipientDetailView,
                    RecipientListView, RecipientUpdateView, start_mailing_view)

app_name = ServerConfig.name


urlpatterns = [
    path("recipient/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipient/view/", RecipientListView.as_view(), name="recipient_list"),
    path(
        "recipient/<int:pk>/update/",
        RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipient/<int:pk>/detail/",
        RecipientDetailView.as_view(),
        name="recipient_detail",
    ),
    path(
        "recipient/<int:pk>/delete/",
        RecipientDeleteView.as_view(),
        name="recipient_confirm_delete",
    ),
    path("message/view/", MessageListView.as_view(), name="message_list"),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path(
        "message/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "message/<int:pk>/detail/", MessageDetailView.as_view(), name="message_detail"
    ),
    path(
        "message/<int:pk>/delete/",
        MessageDeleteView.as_view(),
        name="message_confirm_delete",
    ),
    path("mailings/", MailingListView.as_view(), name="mailing_list"),
    path("mailings/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("", IndexView.as_view(), name="index"),
    path("mailing/create/", MailingCreateView.as_view(), name="mailing_create"),
    path(
        "mailing/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"
    ),
    path(
        "mailing/<int:pk>/delete/",
        MailingDeleteView.as_view(),
        name="mailing_confirm_delete",
    ),
    path(
        "mailing_attempt/",
        MailingAttemptListView.as_view(),
        name="mailing_attempt_list",
    ),
    path(
        "mailing_attempt/<int:pk>/",
        MailingAttemptDetailView.as_view(),
        name="mailing_attempt_detail",
    ),
    path(
        "mailing_attempt/create/",
        MailingAttemptCreateView.as_view(),
        name="mailing_attempt_create",
    ),
    path(
        "mailing_attempt/<int:pk>/update/",
        MailingAttemptUpdateView.as_view(),
        name="mailing_attempt_update",
    ),
    path(
        "mailing_attempt/<int:pk>/delete/",
        MailingAttemptDeleteView.as_view(),
        name="mailing_attempt_confirm_delete",
    ),
]
