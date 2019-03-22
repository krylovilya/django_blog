from django import forms

from .models import User, Post


class RegisterAuthForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = forms.IntegerField(help_text="Captcha")

    class Meta:
        model = User
        fields = ['username', 'password']


class EditForm(forms.ModelForm):
    title = forms.CharField(max_length=150, label="Заголовок")
    content = forms.CharField(max_length=10000, widget=forms.Textarea, label="Содержимое")

    class Meta:
        model = Post
        fields = ['title', 'content']
