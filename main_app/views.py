import base64
import random

from captcha.image import ImageCaptcha
from django.contrib.auth import hashers
from django.contrib.auth import login, logout
from django.http.response import HttpResponse, HttpResponseServerError, Http404
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import RegisterAuthForm, EditForm
from .models import Captcha, User, Post


class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.GET.get('pagination'):
            pagination = int(request.GET['pagination'])
        else:
            pagination = 1
        posts = Post.objects.all().order_by("-created_at")
        if (User.objects.count() / 50).is_integer():
            max_pagination = User.objects.count() / 50
        else:
            max_pagination = User.objects.count() // 50 + 1
        content = {
            "posts": posts,
            "pagination": pagination,
            "max_pagination": max_pagination
        }
        if "msg" in request.GET:
            content.update({"msg": request.GET['msg']})
        return render(request, "index.html", content)


class ProfileView(TemplateView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs['id']
        if user_id == 0:
            return redirect("/profile/{}".format(request.user.id))
        if User.objects.filter(id=user_id).count() == 0:
            raise Http404
        if request.GET.get('pagination'):
            pagination = int(request.GET['pagination'])
        else:
            pagination = 1
        if (User.objects.count() / 50).is_integer():
            max_pagination = User.objects.count() / 50
        else:
            max_pagination = User.objects.count() // 50 + 1
        user_object = User.objects.get(id=user_id)
        posts = Post.objects.filter(author=user_object).order_by("-created_at")[50 * (pagination - 1):50 * pagination]
        content = {
            "current_user": user_object,
            "posts": posts,
            "post_count": Post.objects.filter(author=user_object).count(),
            "pagination": pagination,
            "max_pagination": max_pagination
        }
        return render(request, "profile.html", content)


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
        form = EditForm()
        if request.user.is_authenticated is False:
            raise Http404
        content = {"form": form}
        if "msg" in request.GET:
            content.update({"msg": request.GET['msg']})
        return render(request, "add_post.html", content)

    def post(self, request, *args, **kwargs):
        form = EditForm(request.POST)
        if request.user.is_authenticated is False:
            raise Http404
        if form.is_valid() is False:
            return render(request, "add_post.html", {"form": form})
        new_post = Post()
        new_post.title = request.POST["title"]
        new_post.content = request.POST["content"]
        new_post.author = request.user
        new_post.save()
        return redirect("/?msg=Пост создан")


class EditPostView(TemplateView):
    def get(self, request, *args, **kwargs):
        post_id = kwargs['id']
        if Post.objects.filter(id=post_id).count() == 0:
            raise Http404
        post = Post.objects.filter(id=post_id)[0]
        if request.user != post.author:
            raise Http404
        form = EditForm()
        form.fields["title"].initial = post.title
        form.fields["content"].initial = post.content
        content = {"form": form}
        if "msg" in request.GET:
            content.update({"msg": request.GET['msg']})
        return render(request, "editor.html", content)

    def post(self, request, *args, **kwargs):
        post_id = kwargs['id']
        form = EditForm(request.POST)
        if Post.objects.filter(id=post_id).count() == 0:
            raise Http404
        post = Post.objects.filter(id=post_id)[0]
        if request.user != post.author:
            raise Http404
        post.title = request.POST["title"]
        post.content = request.POST["content"]
        post.save()
        return redirect("/?msg=Пост отредактирован")
