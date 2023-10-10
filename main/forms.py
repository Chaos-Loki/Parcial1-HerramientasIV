from dataclasses import field, fields
from django import forms
from .models import ContactProfile, Blog, Categoria, Producto
#from .models import ContactProfile, BlogPost

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

class BlogPostForm(forms.ModelForm):

	class Meta:
		model = Blog
		fields = ('author','name', 'image', 'description', 'body')


#----------------------------------------------------------

#Formulario para categorias
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']


#Formulario para productos
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'imagen', 'categoria']
    
    # Añade widgets para personalizar la apariencia del formulario si es necesario
    widgets = {
        'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        'categoria': forms.Select(attrs={'class': 'form-control'}),
    }