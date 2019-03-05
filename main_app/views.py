import random

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import hashers
from .forms import RegisterForm
from captcha.image import ImageCaptcha
import base64
from .models import Captcha

class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        content = {}
        if "msg" in request.GET:
            content.update({"msg": request.GET['msg']})
        return render(request, "index.html", content)


class ProfileView(TemplateView):
    def get(self, request, *args, **kwargs):
        pass


class AuthView(TemplateView):
    def get(self, request, *args, **kwargs):
        pass


class RegisterView(TemplateView):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        image = ImageCaptcha(fonts=['main_app/static/Roboto-Regular.ttf'])
        captcha_int = random.randint(1000, 9999)
        data = image.generate("{}".format(captcha_int))
        # image.write('1234', 'out.png')
        # print(request.COOKIES['sessionid'])
        Captcha.create_captcha(request.COOKIES['sessionid'], captcha_int)
        content = {
            'form': form,
            'captcha': base64.b64encode(data.getvalue()).decode(),
        }
        if "msg" in request.GET:
            content.update({"msg": request.GET['msg']})
        return render(request, "register.html", content)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if int(form.data['captcha']) == int(Captcha.get_captcha(request.COOKIES['sessionid'])):
            if form.is_valid():
                new_user = form.save(commit=False)
                new_user.password = hashers.make_password(request.POST['password'])
                new_user.save()
                return redirect("/?msg=Вы успешно зарегистрировались")
            else:
                return render(request, "register.html", {'form': form})
        else:
            return redirect("/register?msg=Неверная капча!")


class AddPostView(TemplateView):
    def get(self, request, *args, **kwargs):
        pass


class EditPostView(TemplateView):
    def get(self, request, *args, **kwargs):
        pass
