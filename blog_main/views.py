# from django.http import HttpResponse
from django.shortcuts import render, redirect
from blogs.models import Blog, Category
from assignment.models import About
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth

def home(request):
  featured_post = Blog.objects.filter(is_featured=True, status='published').order_by('-updated_at')
  posts = Blog.objects.filter(is_featured=False, status='published').order_by('-updated_at')
  try:
    about = About.objects.get(id=1)
  except About.DoesNotExist:
    about = None
  context = {
    'featured_post': featured_post,
    'posts': posts,
    'about': about
  }
  return render(request, 'home.html', context)

def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      # Success message
      messages.success(request, 'Registration successful. Please login to continue.')
      return redirect('register')
  else:
    form = RegistrationForm()
  context = {
    'form': form
  }
  return render(request, 'register.html', context)

def login(request):
  if request.method == 'POST':
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = auth.authenticate(username=username, password=password)
      if user is not None:
        auth.login(request, user)
        return redirect('home')
      else:
        messages.error(request, 'Invalid username or password.')
    else:
      messages.error(request, 'Invalid username or password.')
  else:
    form = AuthenticationForm()
  context = {
    'form': form
  }
  return render(request, 'login.html', context)

def logout(request):
  auth.logout(request)
  return redirect('home')