from django.urls import path
from . import views

urlpatterns = [
  path('<slug:category_slug>/', views.post_by_category, name='post_by_category'),
]