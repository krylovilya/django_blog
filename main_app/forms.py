from .models import User
from django import forms


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = forms.IntegerField(help_text="Captcha")

    class Meta:
        model = User
        fields = ['username', 'password']
