from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from . models import Category, Blog, Comment
from django.db.models import Q

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

def post_detail(request, slug):
  try:
    post = Blog.objects.get(slug=slug, status='published')
    comments = Comment.objects.filter(blog=post).order_by('-created_at')
    if request.method == 'POST':
      comment = Comment(blog=post, user=request.user, comment=request.POST.get('comment'))
      comment.save()
      return redirect('post_detail', slug=slug)
  except Blog.DoesNotExist:
    return redirect('home')
  context = {
    'post': post,
    'comments': comments
  }
  return render(request, 'post_detail.html', context)

def search(request):
  keyword = request.GET.get('keyword')
  posts = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword), status='published').order_by('-updated_at')
  context = {
    'keyword': keyword,
    'posts': posts
  }
  return render(request, 'search.html', context)