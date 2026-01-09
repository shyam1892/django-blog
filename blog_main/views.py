# from django.http import HttpResponse
from django.shortcuts import render
from blogs.models import Blog, Category
from assignment.models import About

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