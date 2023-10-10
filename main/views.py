from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import (
		UserProfile,
		Blog,
		Portfolio,
		Testimonial,
		Certificate,
		Categoria,
		Producto
	)
from django.views import generic
from . forms import ContactForm, CreateUserForm, BlogPostForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.cache import cache_control

from django.urls import reverse


from .forms import CategoriaForm, ProductoForm

#Funcion de Registro
def registerPage(request):
	if request.user.is_authenticated:
		return redirect("main:home")
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)
				return redirect('main:login')
			

		context = {'form':form}
		return render(request, 'main/register.html', context)
#Funcion de Login
def loginPage(request):
	if request.user.is_authenticated:
		return redirect("main:home")
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect("main:home")
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'main/login.html', context)

#Funcion de Logout
def logoutUser(request):
	logout(request)
	return redirect('main:login')

#Funcion de blogcreatepage, aka creacion de la pagina de blog.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='main:login')
def blogCreatePage(request):
	if request.method == 'POST':
		form = BlogPostForm(request.POST, request.FILES)	
		if form.is_valid():
			entrada = form.save()
			messages.success(request, "Se añadio post satisfactoriamente!")
			return redirect('/')
	else:
		form = BlogPostForm()
	return render(request, "main/blog-create.html", {'form':form})

class IndexView(generic.TemplateView):
	template_name = "main/index.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		testimonials = Testimonial.objects.filter(is_active=True)
		certificates = Certificate.objects.filter(is_active=True)
		blogs = Blog.objects.filter(is_active=True)
		portfolio = Portfolio.objects.filter(is_active=True)
		
		context["testimonials"] = testimonials
		context["certificates"] = certificates
		context["blogs"] = blogs
		context["portfolio"] = portfolio
		return context


class ContactView(generic.FormView):
	template_name = "main/contact.html"
	form_class = ContactForm
	success_url = "/"
	
	def form_valid(self, form):
		form.save()
		messages.success(self.request, 'Thank you. We will be in touch soon.')
		return super().form_valid(form)


class PortfolioView(generic.ListView):
	model = Portfolio
	template_name = "main/portfolio.html"
	paginate_by = 10

	def get_queryset(self):
		return super().get_queryset().filter(is_active=True)


class PortfolioDetailView(generic.DetailView):
	model = Portfolio
	template_name = "main/portfolio-detail.html"

class BlogView(generic.ListView):
	model = Blog
	template_name = "main/blog.html"
	paginate_by = 10
	
	def get_queryset(self):
		return super().get_queryset().filter(is_active=True)

class BlogDetailView(generic.DetailView):
	model = Blog
	template_name = "main/blog-detail.html"



#-------------------------------------------------------------

#Lista de categorias
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'main/lista_categorias.html', {'categorias': categorias})

#Vista de nueva categoria
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')  # Redirige a la lista de categorías después de crear una nueva
    else:
        form = CategoriaForm()
    return render(request, 'main/crear_categoria.html', {'form': form})


#Vista de Categoria Existente
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'main/editar_categoria.html', {'form': form, 'categoria': categoria})


#Vista para eliminar una una categoria
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('lista_categorias')
    return render(request, 'main/confirmar_eliminar_categoria.html', {'categoria': categoria})


#---------

#Vista para crear producto
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'main/crear_producto.html', {'form': form})

#Vista para ver la lista de productos
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'mani/lista_productos.html', {'productos': productos})

#Vista para editar productos
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'main/editar_producto.html', {'form': form, 'producto': producto})

#Vista para eliminar producto
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'main/confirmar_eliminar_producto.html', {'producto': producto})