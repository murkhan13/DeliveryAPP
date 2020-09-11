from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User

class LoginForm(forms.Form):
    phone = forms.IntegerField(label = 'Ваш номер телефона')
    password = forms.CharField(widget = forms.PasswordInput)

class VerifyForm(forms.Form):
    key = forms.IntegerField(label = 'Пожалуйста введите OTP-код')


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone', )

    def clean_phone(self):
        phone = self.cleaned_data('phone')
        qs = User.objects.filter(phone=phone)
        if qs.exists():
            raise forms.ValidationError("Данный номер телефона уже используется")
        return phone

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2

class TempRegisterForm(forms.Form):
    phone = forms.IntegerField()
    otp = forms.IntegerField()


class SetPasswordForm(forms.Form):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Подтверждение пароля", widget=forms.PasswordInput)

class UserAdminCreationForm(forms.ModelForm):
    # Form for creating new users. Include all the required
    # field, plus a repeated password."""

    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone', )

        def clean_password2(self):
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError('Пароли не совпадают')
            return password2

        def save(self, commit=True):
            # Save the provided password in a hashed format
            user = super(UserAdminCreationForm, self).save(commit=False)
            user.set_password(self.cleaned_data["password1"])
            # user.active = false
            if commit:
                user.save()
            return user


class UserAdminChangeForm(forms.ModelForm):
    """ A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field. """

    class Meta:
        model = User
        fields = ('phone', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the 
        # field does not have access to the initial value
        return self.initial["password"]


