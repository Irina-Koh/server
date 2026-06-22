from django.contrib import admin
from server.models import Recipient, Message,Mailing,MailingAttempt

@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'comment'
    )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'topic',
        'body'

    )

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        'message',
        'status',
        'start_time',
        'end_time'
    )

admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = (
        'mailing',
        'attempt_time',
        'status',
        'server_response'
    )
