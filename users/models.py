from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    last_name = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Введите имя"
    )
    first_name = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Введите фамилию"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
