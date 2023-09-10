from dataclasses import field, fields
from django import forms
from .models import ContactProfile

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class ContactForm(forms.ModelForm):

	name = forms.CharField(max_length=100, required=True,
		widget=forms.TextInput(attrs={
			'placeholder': '*Full name..',
			}))
	email = forms.EmailField(max_length=254, required=True, 
		widget=forms.TextInput(attrs={
			'placeholder': '*Email..',
			}))
	message = forms.CharField(max_length=1000, required=True, 
		widget=forms.Textarea(attrs={
			'placeholder': '*Message..',
			'rows': 6,
			}))


	class Meta:
		model = ContactProfile
		fields = ('name', 'email', 'message',)

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','email','password1','password2']