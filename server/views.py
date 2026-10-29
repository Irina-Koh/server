from pyexpat.errors import messages

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views.generic.base import TemplateView

from .forms import MailingAttemptForm, MailingForm, MessageForm, RecipientForm
from .models import Mailing, MailingAttempt, Message, Recipient


class RecipientListView(ListView):
    model = Recipient
    template_name = "server/recipient_list.html"
    context_object_name = "recipients"


class RecipientCreateView(CreateView):
    model = Recipient
    template_name = "server/recipient_create.html"
    form_class = RecipientForm
    success_url = reverse_lazy("server:recipient_list")


class RecipientUpdateView(UpdateView):
    model = Recipient
    template_name = "server/recipient_update.html"
    form_class = RecipientForm

    def get_success_url(self):
        """
        Возвращает URL-адрес, на который будет перенаправлен пользователь
        после успешной обработки формы.
        """
        return reverse("server:recipient_detail", kwargs={"pk": self.object.pk})


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = "server/recipient_detail.html"
    context_object_name = "recipients"


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "server/recipient_confirm_delete.html"
    success_url = reverse_lazy("server:recipient_list")
    permission_required = "server.delete_recipient"


class MessageListView(ListView):
    model = Message
    template_name = "server/message_list.html"
    context_object_name = "messages"


class MessageCreateView(CreateView):
    model = Message
    template_name = "server/message_create.html"
    form_class = MessageForm
    success_url = reverse_lazy("server:message_list")


class MessageUpdateView(UpdateView):
    model = Message
    template_name = "server/message_update.html"
    form_class = MessageForm

    def get_success_url(self):
        return reverse("server:message_detail", kwargs={"pk": self.object.pk})


class MessageDetailView(DetailView):
    model = Message
    template_name = "server/message_detail.html"
    context_object_name = "messages"


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "server/message_confirm_delete.html"
    success_url = reverse_lazy("server:message_list")
    permission_required = "server.delete_message"


def start_mailing_view(request, pk):
    """
    Представление для запуска рассылки по клику в интерфейсе.
    """
    mailing = get_object_or_404(Mailing, pk=pk)

    try:
        mailing.process_manual_start()
    except Exception as e:
        # Сообщаем пользователю об ошибке, если окно времени неактивно
        messages.error(request, str(e))

    return redirect("mailing_detail", pk=mailing.pk)


class IndexView(TemplateView):
    template_name = "server/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        total_mailings = Mailing.objects.count()
        active_mailings = Mailing.objects.filter(
            start_time__lte=now, end_time__gte=now
        ).count()
        total_recipients = Recipient.objects.count()

        context.update(
            {
                "total_mailings": total_mailings,
                "active_mailings": active_mailings,
                "total_recipients": total_recipients,
            }
        )
        return context


class MailingListView(ListView):
    """
    Представление для отображения списка всех рассылок.
    """

    model = Mailing
    template_name = "server/mailing_list.html"  # Создадим этот файл
    context_object_name = "mailings"  # Имя переменной в шаблоне


class MailingDetailView(DetailView):
    """
    Представление для отображения детальной информации о рассылке,
    включая все связанные попытки отправки.
    """

    model = Mailing
    template_name = "server/mailing_detail.html"
    context_object_name = "mailing"

    def get_context_data(self, **kwargs):
        """
        Добавляет в контекст информацию о попытках отправки.
        """
        # Сначала получаем базовый контекст
        context = super().get_context_data(**kwargs)

        # Получаем объект рассылки из self.object
        mailing = self.object

        # Запрашиваем все попытки этой рассылки и добавляем их в контекст
        attempts = mailing.attempts.all()  # Используется related_name='attempts'
        context["attempts"] = attempts

        return context


class MailingCreateView(CreateView):
    model = Mailing
    template_name = "server/mailing_create.html"
    form_class = MailingForm
    success_url = reverse_lazy("server:mailing_list")


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = "server/mailing_update.html"
    form_class = MailingForm
    success_url = reverse_lazy("server:mailing_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "server/mailing_confirm_delete.html"
    success_url = reverse_lazy("server:mailing_list")
    permission_required = "server.delete_mailing"


class MailingAttemptListView(ListView):
    """
    Представление для отображения списка всех рассылок.
    """

    model = MailingAttempt
    template_name = "server/mailing_attempt_list.html"  # Создадим этот файл
    context_object_name = "mailingAttempt"


class MailingAttemptDetailView(DetailView):
    """
    Представление для отображения детальной информации о рассылке,
    включая все связанные попытки отправки.
    """

    model = MailingAttempt
    template_name = "server/mailing_attempt_detail.html"
    context_object_name = "mailing_attempt"


class MailingAttemptCreateView(CreateView):
    model = MailingAttempt
    template_name = "server/mailing_attempt_create.html"
    form_class = MailingAttemptForm
    success_url = reverse_lazy("server:mailing_attempt_list")


class MailingAttemptUpdateView(UpdateView):
    model = Mailing
    template_name = "server/mailing_attempt_update.html"
    form_class = MailingAttemptForm

    success_url = reverse_lazy("server:mailing_attempt_list")


class MailingAttemptDeleteView(DeleteView):
    model = MailingAttempt
    template_name = "server/mailing_attempt_confirm_delete.html"
    success_url = reverse_lazy("server:mailing_attempt_list")
    permission_required = "server.delete_mailing_attempt"
