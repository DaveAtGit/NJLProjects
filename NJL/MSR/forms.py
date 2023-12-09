from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import FileTransfer


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileTransfer
        fields = ('name', 'file', )


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=64, help_text='Required, enter valid email io_address')
    # model = Employee.user

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    # model = Employee.user

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid login')
