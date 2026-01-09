from django.db import models

# Create your models here.
class About(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = 'About'
    verbose_name_plural = 'About'

  def __str__(self):
    return self.title
  
class SocialLinks(models.Model):
  name = models.CharField(max_length=100)
  link = models.URLField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = 'SocialLinks'
    verbose_name_plural = 'Social Links'

  def __str__(self):
    return self.name