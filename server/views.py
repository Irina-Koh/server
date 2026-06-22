from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, redirect
from .models import Mailing, Recipient
from django.views.generic import TemplateView
from django.utils import timezone

class MailingDetailView(DetailView):
    model = Mailing

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        # Обновляем статус при каждом просмотре страницы рассылки
        obj.update_status()
        return obj

# Для запуска рассылки вручную из интерфейса можно использовать FormView или отдельную функцию/API-эндпоинт.
# Пример простой функции для запуска:


def run_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    try:
        mailing.send_messages()
    except Exception as e:
        # Обработка ошибки (например, вывод сообщения пользователю)
        pass # В реальном проекте используйте messages framework или логирование
    return redirect('mailing_detail', pk=pk)



class IndexView(TemplateView):
    template_name = "server/messages_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        # Общее количество рассылок
        context['total_mailings'] = Mailing.objects.count()

        # Количество активных рассылок (статус 'Запущена')
        context['active_mailings'] = Mailing.objects.filter(
            start_time__lte=now,
            end_time__gte=now,
            status='Запущена'
        ).count()

        # Количество уникальных получателей
        context['total_recipients'] = Recipient.objects.count()

        return context