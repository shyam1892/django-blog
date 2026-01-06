# from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from . models import Category, Blog

# Create your views here.
def post_by_category(request, category_slug):
  # To show 404 page if category is not found then create a page as 404.html and make debug false
  # category = get_object_or_404(Category, category_slug=category_slug)
  try:
    category = Category.objects.get(category_slug=category_slug)
  except Category.DoesNotExist:
    return redirect('home')
  posts = Blog.objects.filter(category__category_slug=category_slug, status='published').order_by('-updated_at')
  context = {
    'category': category,
    'posts': posts
  }
  return render(request, 'post_by_category.html', context)