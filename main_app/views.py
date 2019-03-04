from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import hashers
from .forms import RegisterForm
import datetime


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
        content = {
            'form': form,
        }
        return render(request, "register.html", content)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.password = hashers.make_password(request.POST['password'])
            new_user.save()
            return redirect("/?msg=Вы успешно зарегистрировались")
        return render(request, "register.html", {'form': form})


class AddPostView(TemplateView):
    def get(self, request, *args, **kwargs):
        pass


class EditPostView(TemplateView):
    def get(self, request, *args, **kwargs):
        pass
