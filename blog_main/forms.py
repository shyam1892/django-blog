from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegistrationForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['email', 'username', 'password1', 'password2']

  # Set email field as required
  def __init__(self, *args, **kwargs):
    super(RegistrationForm, self).__init__(*args, **kwargs)
    self.fields['email'].required = True

  # Set email field as unique
  def clean_email(self):
    email = self.cleaned_data['email']
    if User.objects.filter(email=email).exists():
      raise forms.ValidationError("Email already exists")
    return email
  
  # Set username field as unique
  def clean_username(self):
    username = self.cleaned_data['username']
    if User.objects.filter(username=username).exists():
      raise forms.ValidationError("Username already exists")
    return username