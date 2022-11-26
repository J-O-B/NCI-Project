from django import forms
from .models import UserProfile, Credential

class ProfileEditForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        label='Name',
        widget=forms.TextInput(attrs={
            'rows': '1',
            'min-length': 6,
        }))
    
    phone = forms.CharField(
        required=True,
        label='Phone',
        widget=forms.TextInput(attrs={
            'rows': '1',
            'min-length': 6,
        }))
    email = forms.EmailField(label=('Email'))
    class Meta:
        model = UserProfile
        fields = ['name', 'phone', 'email']

class CredentialForm(forms.ModelForm):
    service = forms.CharField(
        required=True,
        label='Service (i.e Facebook)',
        widget=forms.TextInput(attrs={
            'rows': '1',
            'min-length': 0,
            'max-length': 100,
        }))
    
    username = forms.CharField(
        required=False,
        label='Username / Email For This Service',
        widget=forms.TextInput(attrs={
            'rows': '1',
            'min-length': 0,
            'max-length': 65,
        }))
    password = forms.CharField(
        required=False,
        label='Password For This Service',
        widget=forms.PasswordInput(attrs={
            'rows': '1',
            'min-length': 0,
            'max-length': 65,
        }))
    phone = forms.CharField(
        required=False,
        label='Phone Number For This Service',
        widget=forms.TextInput(attrs={
            'rows': '1',
            'min-length': 0,
            'max-length': 65,
        }))

    email = forms.EmailField(label=('Email'))

    class Meta:
        model = Credential
        fields = ['service', 'username', 'password', 'phone', 'email']