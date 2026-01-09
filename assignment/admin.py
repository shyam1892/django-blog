from django.contrib import admin
from .models import About, SocialLinks

# Register your models here.
class AboutAdmin(admin.ModelAdmin):
  list_display = ['title', 'description']
  # Can be add only once
  def has_add_permission(self, request):
    data_count = About.objects.count()
    if data_count == 1:
      return False
    else:
      return True

class SocialLinksAdmin(admin.ModelAdmin):
  list_display = ['name', 'link']

admin.site.register(About, AboutAdmin)
admin.site.register(SocialLinks, SocialLinksAdmin)

