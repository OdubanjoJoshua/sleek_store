from django import forms
from django.forms import ModelForm
from . models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# form for contact
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'message']

# form for Checkout
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ['full_name', 'address_1', 'address_2', 'zip_code', 'phone', 'use_or_not']


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'label':'border:10px solid #d0cccc'}))
    # first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'label':'border:10px solid #d0cccc'}))
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'style':'border:10px solid #d0cccc'}))
    email = forms.EmailField(max_length=50, required=True, widget=forms.TextInput(attrs={'style':'border:10px solid #d0cccc'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']



# form for updated user
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
                'username':forms.TextInput(attrs={'class':'form-input', 'label':'border:10px solid #d0cccc'}),
                'first_name':forms.TextInput(attrs={'class':'form-input'}),
                'last_name':forms.TextInput(attrs={'class':'form-input'}),
                'email':forms.TextInput(attrs={'class':'form-input'}),
        }

