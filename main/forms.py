from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models import User


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        def save(self, commit=True):
            user = super(NewUserForm, self).save(commit=False)
            user.email = self.cleaned_data["email"]
            if commit:
                user.save()
            return user


class ForgotForm(forms.Form):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = "email"


class PassForm(forms.Form):
    password1 = forms.CharField(
        required=True, max_length=50, widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        required=True, max_length=50, widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ("password1", "password2")


class UserDataForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    name = forms.CharField(required=True)
    lastname = forms.CharField(required=True)
    number = forms.RegexField(
        regex=r"^[1-9][0-9]{2}-?[0-9]{3}-?[0-9]{3}$", required=True
    )
    address = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "name", "lastname", "number", "address")
