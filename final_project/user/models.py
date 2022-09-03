from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    register_date = models.DateTimeField(auto_now_add=True, verbose_name="등록날짜")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자"
