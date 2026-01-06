from django.contrib import admin
from .models import Category, Blog

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'category_slug': ('category_name',)}
  list_display = ('category_name', 'category_slug')
  list_filter = ('category_name',)
  search_fields = ('category_name',)

admin.site.register(Category, CategoryAdmin)

class BlogAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('title',)}
  list_display = ('title', 'slug', 'category', 'author', 'status', 'is_featured')
  list_filter = ('status', 'is_featured')
  search_fields = ('title', 'category__category_name', 'status')
  list_editable = ('is_featured',)

admin.site.register(Blog, BlogAdmin)
