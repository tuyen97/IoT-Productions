from django import forms
from pas.models import Member


class LoginForm(forms.ModelForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter email'
    }))
    password = forms.CharField(label='Pass word', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter email'
    }))

    class Meta:
        model = Member
        fields = ['email', 'password']

