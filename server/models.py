from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models, transaction
from django.utils import timezone


class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(
        max_length=100,
        verbose_name="Имя",
        blank=True,
        help_text="Введите имя получателя",
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="Фамилия",
        blank=True,
        help_text="Введите фамилию получателя",
    )
    comment = models.TextField(
        verbose_name="Комментарий",
        blank=True,
        null=True,
        help_text="Дополнительная информация о получателе",
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"


class Message(models.Model):
    subject = models.CharField(
        max_length=200, verbose_name="Тема письма", help_text="Введите тему письма"
    )
    body = models.TextField(
        verbose_name="Текст письма", help_text="Введите текст письма"
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


# --- Модели для управления рассылками ---


class MailingAttempt(models.Model):
    mailing = models.ForeignKey(
        "Mailing", on_delete=models.CASCADE, related_name="attempts"
    )
    recipient = models.ForeignKey(Recipient, on_delete=models.SET_NULL, null=True)
    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=[("Успешно", "Успешно"), ("Не успешно", "Не успешно")]
    )
    server_response = models.TextField(blank=True)

    class Meta:
        verbose_name = "Попытка отправки"
        verbose_name_plural = "Попытки отправки"


class Mailing(models.Model):
    STATUS_CHOICES = [
        ("Создана", "Создана"),
        ("Запущена", "Запущена"),
        ("Завершена", "Завершена"),
    ]

    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Создана")

    def clean(self):
        """Валидация дат перед сохранением."""
        now = timezone.now()
        if self.start_time < now:
            raise ValidationError(
                "Дата и время начала отправки не могут быть в прошлом."
            )
        if self.start_time >= self.end_time:
            raise ValidationError("Дата начала должна быть раньше даты окончания.")

    def update_status(self):
        """
        Динамическое обновление статуса рассылки.
        Этот метод НЕ сохраняет объект автоматически, он только меняет атрибут.
        Сохранение следует вызывать отдельно, если статус изменился.
        """

        # Динамический статус (рекомендуется вычислять при каждом обращении)

    @property
    def current_status(self):
        """Вычисляет текущий статус рассылки."""
        now = timezone.now()
        if now < self.start_time:
            return "Создана"
        elif self.start_time <= now <= self.end_time:
            return "Запущена"
        else:
            return "Завершена"

    @transaction.atomic
    def process_manual_start(self):
        """
        Ручной запуск рассылки.
        Создает записи о попытках отправки для каждого получателя.
        """
        if not (self.start_time <= timezone.now() <= self.end_time):
            raise Exception("Рассылку нельзя запустить вручную вне временного окна.")

        attempts = []
        for recipient in self.recipients.all():
            try:
                send_mail(
                    self.message.subject,
                    self.message.body,
                    "Rakhmankulova1991@ya.ru",
                    [recipient.email],
                    fail_silently=False,
                )
                attempts.append(
                    MailingAttempt(
                        mailing=self,
                        recipient=recipient,
                        status="Успешно",
                        server_response="Письмо отправлено успешно",
                    )
                )
            except Exception as e:
                attempts.append(
                    MailingAttempt(
                        mailing=self,
                        recipient=recipient,
                        status="Ошибка",
                        server_response=str(e),
                    )
                )

        # Сохраняем все попытки одной операцией БД
        if attempts:
            MailingAttempt.objects.bulk_create(attempts)
