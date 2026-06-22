from datetime import timezone
from django.db import models
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class Recipient(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name='Имя',
        blank=True,
        help_text='Введите имя получателя'
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Фамилия',
        blank=True,
        help_text='Введите фамилию получателя'
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True,
        null=True,
        help_text='Дополнительная информация о получателе'
    )


    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'


class Message(models.Model):
    topic = models.CharField(
        max_length=200,
        verbose_name='Тема письма',
        help_text='Введите тему письма'
    )
    body = models.TextField(
        verbose_name='Текст письма',
        help_text='Введите текст письма'
    )

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MailingAttempt(models.Model):
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, related_name='attempts')
    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('Успешно', 'Успешно'),
        ('Не успешно', 'Не успешно')
    ])
    server_response = models.TextField(blank=True)



class Mailing(models.Model):
    STATUS_CHOICES = [
        ('Создана', 'Создана'),
        ('Запущена', 'Запущена'),
        ('Завершена', 'Завершена'),
    ]

    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Создана')

    def clean(self):
        """Валидация дат перед сохранением."""
        now = timezone.now()
        if self.start_time < now:
            raise ValidationError("Дата и время начала отправки не могут быть в прошлом.")
        if self.start_time >= self.end_time:
            raise ValidationError("Дата начала должна быть раньше даты окончания.")

    def update_status(self):
        """Динамическое обновление статуса и сохранение в БД."""
        now = timezone.now()
        if self.start_time > now:
            new_status = 'Создана'
        elif self.start_time <= now <= self.end_time:
            new_status = 'Запущена'
        else:
            new_status = 'Завершена'

        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=['status'])

    def send_messages(self):
        """
        Метод для запуска рассылки.
        Создает записи о попытках отправки для каждого получателя.
        """
        

        if not (self.start_time <= timezone.now() <= self.end_time):
            raise Exception("Рассылка не может быть запущена: текущее время вне окна отправки.")

        for recipient in self.recipients.all():
            try:
                send_mail(
                    self.message.subject,
                    self.message.body,
                    'Rakhmankulova1991@ya.ru',  # Укажите свой адрес отправителя в settings.py (DEFAULT_FROM_EMAIL)
                    [recipient.email],
                    fail_silently=False,
                )
                MailingAttempt.objects.create(
                    mailing=self,
                    status='Успешно',
                    server_response='Письмо отправлено успешно'
                )
            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=self,
                    status='Не успешно',
                    server_response=str(e)
                )

