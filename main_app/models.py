from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=150, unique=True, verbose_name="Логин")
    password = models.CharField(max_length=150, blank=True, verbose_name="Пароль")
    last_login = models.DateTimeField(blank=True, verbose_name="Последний вход", editable=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    content = models.TextField(max_length=10000, verbose_name="Текст")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return "{} (Автор: {})".format(self.title, self.author)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
