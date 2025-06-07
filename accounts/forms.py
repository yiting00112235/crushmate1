# accounts/forms.py
# 這是signup用來驗證你輸入的東西是我們要的的地方
# 這邊是django-allauth沒有的一些功能, 像是upper lower case這種

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
import allauth.account.forms as allauth_forms


class CustomSignupForm(allauth_forms.SignupForm):
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if any(c.isupper() for c in username):
            raise forms.ValidationError("Username cannot contain uppercase letters.")
        return username
    
class CustomLoginForm(allauth_forms.LoginForm):
    def clean_login(self):
        login = self.cleaned_data.get("login")
        user = authenticate(username=login, password=self.cleaned_data.get("password"))

        # 如果帳號存在但 username 大小寫不同，就讓它失敗
        from django.contrib.auth.models import User
        try:
            user_exact = User.objects.get(username=login)
        except User.DoesNotExist:
            raise ValidationError("This username is not registered.")
        
        if user_exact.username != login:
            raise ValidationError("Username must match exactly (case-sensitive).")

        return login