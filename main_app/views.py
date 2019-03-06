import base64
import random

from captcha.image import ImageCaptcha
from django.contrib.auth import hashers
from django.contrib.auth import login, logout
from django.http.response import HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import RegisterAuthForm
from .models import Captcha, User


class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        content = {}
        if "msg" in request.GET:
            content.update({"msg": request.GET['msg']})
        return render(request, "index.html", content)


class ProfileView(TemplateView):
    def get(self, request, *args, **kwargs):
        pass


def generate_captcha():
    image = ImageCaptcha()
    captcha_int = random.randint(1000, 9999)
    captcha_id = random.randint(10000, 99999)
    data = image.generate("{}".format(captcha_int))
    image_base64 = base64.b64encode(data.getvalue()).decode()
    Captcha.create_captcha(captcha_id, captcha_int)
    return {"id": captcha_id,
            "int": captcha_int,
            "image": image_base64}


class AuthView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.session.test_cookie_worked() is not True:
            request.session.set_test_cookie()
            if 'cookie_check' in request.GET:
                return HttpResponse("Please enable cookies and try again.")
            return redirect("/auth?cookie_check=1")
        form = RegisterAuthForm()
        new_captcha = generate_captcha()
        content = {
            'form': form,
            'captcha': new_captcha['image'],
        }
        if "msg" in request.GET:
            content.update({"msg": request.GET['msg']})
        response = render(request, "auth.html", content)
        response.set_cookie(key="captcha", value=new_captcha['id'])
        return response

    def post(self, request, *args, **kwargs):
        form = RegisterAuthForm(request.POST)
        if "captcha" in request.COOKIES:
            captcha_id = request.COOKIES['captcha']
            captcha_int = Captcha.get_captcha(captcha_id)
        else:
            return HttpResponse("Cookies error!")
        if int(form.data['captcha']) == int(captcha_int):
            enter_password = request.POST['password']
            user_object = User.objects.filter(username=request.POST['username'])[0]
            if hashers.check_password(str(enter_password), str(user_object.password)):
                login(request, user_object)
                return redirect("/?msg=Добро пожаловать, {}".format(user_object.username))
            else:
                return redirect("/auth?msg=Неверный логин или пароль!")
        else:
            return redirect("/auth?msg=Неверная капча!")


class RegisterView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.session.test_cookie_worked() is not True:
            request.session.set_test_cookie()
            if 'cookie_check' in request.GET:
                return HttpResponse("Please enable cookies and try again.")
            return redirect("/register?cookie_check=1")
        form = RegisterAuthForm()
        new_captcha = generate_captcha()
        content = {
            'form': form,
            'captcha': new_captcha['image'],
        }
        if "msg" in request.GET:
            content.update({"msg": request.GET['msg']})
        response = render(request, "register.html", content)
        response.set_cookie(key="captcha", value=new_captcha['id'])
        return response

    def post(self, request, *args, **kwargs):
        form = RegisterAuthForm(request.POST)
        if "captcha" in request.COOKIES:
            captcha_id = request.COOKIES['captcha']
            captcha_int = Captcha.get_captcha(captcha_id)
        else:
            return HttpResponse("Cookies error!")
        if int(form.data['captcha']) == int(captcha_int):
            if form.is_valid():
                new_user = form.save(commit=False)
                new_user.password = hashers.make_password(request.POST['password'])
                new_user.save()
                return redirect("/?msg=Вы успешно зарегистрировались")
            else:
                new_captcha = generate_captcha()
                response = render(request, "register.html", {'form': form, 'captcha': new_captcha['image']})
                response.set_cookie(key="captcha", value=new_captcha['id'])
                return response
        else:
            return redirect("/register?msg=Неверная капча!")


class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return redirect("/")
        else:
            return HttpResponseServerError


class AddPostView(TemplateView):
    def get(self, request, *args, **kwargs):
        pass


class EditPostView(TemplateView):
    def get(self, request, *args, **kwargs):
        pass
