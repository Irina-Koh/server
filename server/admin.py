from django.contrib import admin

from .models import Mailing, MailingAttempt, Message, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    """
    Настройка интерфейса администратора для модели Recipient.
    """

    # Поля, которые будут видны в списке получателей
    list_display = ("email", "first_name", "last_name")

    # Добавляем строку поиска по указанным полям
    search_fields = ("email", "first_name", "last_name")

    # Можно добавить фильтрацию по полю комментария (есть/нет)
    list_filter = ("comment",)

    # Группируем поля на странице редактирования для удобства
    fieldsets = (
        ("Контактная информация", {"fields": ("email",)}),
        ("Личная информация", {"fields": ("first_name", "last_name")}),
        (
            "Дополнительно",
            {
                "fields": ("comment",),
                "classes": ("collapse",),  # Поле будет свернуто по умолчанию
            },
        ),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Настройка интерфейса администратора для модели Message.
    """

    # В списке сообщений показываем тему и первые 50 символов текста
    list_display = ("subject", "body_preview")

    # Строка поиска по теме письма
    search_fields = ("subject",)

    def body_preview(self, obj):
        """
        Метод для отображения превью текста письма в списке.
        Возвращает первые 50 символов.
        """
        return obj.body[:50] + "..." if len(obj.body) > 50 else obj.body

    body_preview.short_description = "Текст письма (превью)"


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    """Настройка отображения попыток отправки в админке."""

    list_display = ("mailing", "recipient", "attempt_time", "status")
    list_filter = ("status", "attempt_time")  # Фильтры справа
    search_fields = ("recipient__email", "server_response")
    readonly_fields = ("attempt_time",)  # Время попытки нельзя менять


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """Настройка отображения рассылок в админке."""

    list_display = ("message", "start_time", "end_time", "get_current_status")
    filter_horizontal = ("recipients",)  # Удобный виджет для выбора многих ко многим
    readonly_fields = ("end_time",)  # Если end_time задается автоматически

    def get_current_status(self, obj):
        """
        Метод для отображения динамического статуса в списке рассылок.
        """
        return obj.current_status

    get_current_status.short_description = "Текущий статус"
