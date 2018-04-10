from django import forms

from django.contrib.auth.models import User
from hireServiceapp.models import Seller

class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name", "email")

class UserFormForEdit(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ("name", "phone", "address", "image")
