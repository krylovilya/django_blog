from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http.response import HttpResponseServerError


# Create your models here.


class User(AbstractUser):
    # username = models.CharField(max_length=150, unique=True, verbose_name="Логин")
    # password = models.CharField(max_length=150, blank=True, verbose_name="Пароль")
    # last_login = models.DateTimeField(verbose_name="Последний вход", editable=False)

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


class Captcha(models.Model):
    # Хорошо бы добавить в crontab задачу, которая удаляет объекты, старше, например, 24 часов
    captcha_id = models.IntegerField()
    captcha_text = models.IntegerField()

    @staticmethod
    def create_captcha(captcha_id, captcha_int):
        if Captcha.objects.filter(captcha_id=captcha_id).count() == 0:
            Captcha.objects.create(captcha_id=captcha_id, captcha_text=captcha_int)
            return
        else:
            captcha = Captcha.objects.get(captcha_id=captcha_id)
            captcha.captcha_text = captcha_int
            captcha.save()

    @staticmethod
    def get_captcha(captcha_id):
        if Captcha.objects.filter(captcha_id=captcha_id).count() == 0:
            raise HttpResponseServerError
        return Captcha.objects.filter(captcha_id=captcha_id)[0].captcha_text
