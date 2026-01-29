from django.shortcuts import render, redirect, get_object_or_404
from blogs.models import Category, Blog
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, BlogForm, AddUserForm, EditUserForm
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='login')
def dashboard(request):
  category_count = Category.objects.count()
  post_count = Blog.objects.count()
  context = {
    'category_count': category_count,
    'post_count': post_count
  }
  return render(request, 'dashboard/dashboard.html', context)

def categories(request):
  return render(request, 'dashboard/categories.html')

def add_category(request):
  if request.method == 'POST':
    form = CategoryForm(request.POST)
    if form.is_valid():
      form.save()
      # Generate a slug based on the cleaned category name
      form.instance.category_slug = slugify(form.cleaned_data['category_name'])+'-'+str(form.instance.id)
      form.save()
      return redirect('categories')
  form = CategoryForm()
  context = {
    'form': form
  }
  return render(request, 'dashboard/add_category.html', context)

def edit_category(request, pk):
  category = get_object_or_404(Category, pk=pk)
  form = CategoryForm(instance=category)
  if request.method == 'POST':
    form = CategoryForm(request.POST, instance=category)
    if form.is_valid():
      form.save()
      # Generate a slug based on the cleaned category name
      form.instance.category_slug = slugify(form.cleaned_data['category_name'])+'-'+str(form.instance.id)
      form.save()
      return redirect('categories')
  context = {
    'form': form,
    'category': category
  }
  return render(request, 'dashboard/edit_category.html', context)

def delete_category(request, pk):
  category = get_object_or_404(Category, pk=pk)
  category.delete()
  return redirect('categories')

def posts(request):
  # If user group is manager then show all posts otherwise show only user posts
  if request.user.groups.filter(name='Manager').exists():
    posts = Blog.objects.all().order_by('-updated_at')
  else:
    posts = Blog.objects.filter(author=request.user).order_by('-updated_at')
  context = {
    'posts': posts
  }
  return render(request, 'dashboard/posts.html', context)

def add_post(request):
  if request.method == 'POST':
    form = BlogForm(request.POST, request.FILES)
    if form.is_valid():
      form.instance.author = request.user
      form.save()
      # Generate a slug based on the cleaned title
      form.instance.slug = slugify(form.cleaned_data['title'])+'-'+str(form.instance.id)
      form.save()
      return redirect('posts')
  form = BlogForm()
  context = {
    'form': form
  }
  return render(request, 'dashboard/add_post.html', context)

def edit_post(request, pk):
  # Find post by author and pk
  if request.user.groups.filter(name='Manager').exists():
    post = Blog.objects.filter(pk=pk).first()
  else:
    post = Blog.objects.filter(author=request.user, pk=pk).first()
  if post:
    form = BlogForm(instance=post)
    if request.method == 'POST':
      form = BlogForm(request.POST, request.FILES, instance=post)
      if form.is_valid():
        form.save()
        # Generate a slug based on the cleaned title
        form.instance.slug = slugify(form.cleaned_data['title'])+'-'+str(form.instance.id)
        form.save()
        return redirect('posts')
    context = {
      'form': form,
      'post': post
    }
    return render(request, 'dashboard/edit_post.html', context)
  else:
    # Post not found message
    messages.error(request, 'Post not found.')
    return redirect('posts')
  
def delete_post(request, pk):
  # Find post by author and pk
  if request.user.groups.filter(name='Manager').exists():
    post = Blog.objects.filter(pk=pk).first()
  else:
    post = Blog.objects.filter(author=request.user, pk=pk).first()
  if post:
    # Delete Image from media folder
    if post.featured_image:
      post.featured_image.delete()
    post.delete()
    return redirect('posts')
  else:
    # Post not found message
    messages.error(request, 'Post not found.')
    return redirect('posts')

def users(request):
  # Find all users except superuser
  users = User.objects.exclude(is_superuser=True).order_by('-date_joined')
  context = {
    'users': users
  }
  return render(request, 'dashboard/users.html', context)

def add_user(request):
  if request.method == 'POST':
    form = AddUserForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('users')
  form = AddUserForm()
  context = {
    'form': form
  }
  return render(request, 'dashboard/add_user.html', context)

def edit_user(request, pk):
  user = get_object_or_404(User, pk=pk)
  form = EditUserForm(instance=user)
  if request.method == 'POST':
    form = EditUserForm(request.POST, instance=user)
    if form.is_valid():
      form.save()
      return redirect('users')
  context = {
    'form': form,
    'user': user
  }
  return render(request, 'dashboard/edit_user.html', context)

def delete_user(request, pk):
  user = get_object_or_404(User, pk=pk)
  user.delete()
  return redirect('users')