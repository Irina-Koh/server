from django import forms
from .models import Mailing, Message, Recipient

class MailingForm(forms.ModelForm):
    """
    Форма для создания рассылки.
    Использует виджеты фильтрации для полей ManyToMany.
    """
    message = forms.ModelChoiceField(queryset=Message.objects.all())
    recipients = forms.ModelMultipleChoiceField(
        queryset=Recipient.objects.all(),
        widget=forms.CheckboxSelectMultiple, # Или FilteredSelectMultiple для админки
        required=True
    )

    class Meta:
        model = Mailing
        fields = ['message', 'recipients', 'start_time', 'end_time']
