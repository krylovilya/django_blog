from django import forms

from .models import User


class RegisterAuthForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = forms.IntegerField(help_text="Captcha")

    class Meta:
        model = User
        fields = ['username', 'password']
