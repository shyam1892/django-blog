from . models import SocialLinks

def get_social_links(request):
  social_links = SocialLinks.objects.all()
  return dict(social_links=social_links)