from django.contrib import admin
from CodeSearchApp import models
from .models import ProfilePage
from .models import Post

admin.site.register(Post)
admin.site.register(ProfilePage)
# Register your models here.
