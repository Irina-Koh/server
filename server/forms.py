from django import forms
from django.core.exceptions import ValidationError

from .models import Mailing, MailingAttempt, Message, Recipient


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = [
            "first_name",
            "last_name",
            "email",
            "comment",
        ]

    def __init__(self, *args, **kwards):
        super(RecipientForm, self).__init__(*args, **kwards)
        self.fields["first_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите имя"}
        )
        self.fields["last_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите фамилию"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите email"}
        )
        self.fields["comment"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите комментарий"}
        )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        if Recipient.objects.filter(email=email):
            raise ValidationError("Получатель с таким email уже существует")
        return cleaned_data


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            "subject",
            "body",
        ]

    def __init__(self, *args, **kwards):
        super(MessageForm, self).__init__(*args, **kwards)
        self.fields["subject"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите тему сообщения"}
        )
        self.fields["body"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите сообщение"}
        )


class MailingAttemptForm(forms.ModelForm):
    class Meta:
        model = MailingAttempt
        fields = [
            "mailing",
            "recipient",
            "status",
        ]

    def __init__(self, *args, **kwards):
        super(MailingAttemptForm, self).__init__(*args, **kwards)
        self.fields["mailing"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Выберите рассылку"}
        )
        self.fields["recipient"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Выберете получателя"}
        )
        self.fields["attempt_time"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите время"}
        )
        self.fields["status"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Статус"}
        )
        self.fields["server_response"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Ответ сервера"}
        )


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = [
            "message",
            "recipients",
            "start_time",
            "status",
            "end_time",
        ]

    def __init__(self, *args, **kwards):
        super(MailingForm, self).__init__(*args, **kwards)
        self.fields["message"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Выберите сообщение"}
        )
        self.fields["recipients"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Выберете получателя"}
        )
        self.fields["start_time"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите время начала"}
        )
        self.fields["status"].widget.attrs.update(
            {"class": "form-control", "placeholder": "выберите статус"}
        )
        self.fields["end_time"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите время окончания"}
        )
