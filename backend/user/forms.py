from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # 将密码加密
        if commit:
            user.save()
        return user
    
    username = forms.CharField(required=True)  # 确保是必填的
    password = forms.CharField(required=True, widget=forms.PasswordInput)  # 同上
