from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    # default widget = TextInput
    # PasswordInput widget이 HTML input 요소를 type="password"로 렌더링 할 때 사용된다.
    password = forms.CharField(widget=forms.PasswordInput)


# from django.contrib.auth.forms import UserCreationForm
# 아래의 클래스는 django에서 위와 같이 유사한 클래스를 제공한다.
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        # model fields
        fields = ('username', 'first_name', 'email')

    # clean_<fieldname>(): 특정 필드의 유효성 검증을 위해 사용
    # 실행시점 : form.is_valid() 호출 시, 아래의 clean_<fieldname>() 메서드가 실행된다.
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']

    def clean_email(self):
        # clean_email은 clean_password2()에서 처리할 수 있지만
        # 명시적으로 분리하는 것이 맞다고 봄
        cd = self.cleaned_data
        try:
            User.objects.get(email=cd['email'])
        except User.DoesNotExist:
            return cd['email']
        raise forms.ValidationError('Email is duplicated.')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        cd = self.cleaned_data
        if 'email' in self.changed_data:
            try:
                User.objects.get(email=cd['email'])
            except User.DoesNotExist:
                return cd['email']
            raise forms.ValidationError('Email is duplicated.')
        else:
            return cd['email']
