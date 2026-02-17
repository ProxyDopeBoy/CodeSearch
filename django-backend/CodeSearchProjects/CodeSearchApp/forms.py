from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory

from .models import ProfilePage, Post, Code


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    def save(self):
        user = User(
            username = self.cleaned_data['username'],
            email = self.cleaned_data['email']
        )
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует')
        return username
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с такой почтой уже существует')
        return email
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class FormUserUpdate(forms.ModelForm):
    class Meta:
        model = ProfilePage
        fields = '__all__'


class DropPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'stack']

PostFormSet = inlineformset_factory(
    parent_model=Post,
    model=Code,
    fields = ('code',),
    extra = 1,
    can_delete = True,
)

