
from django.shortcuts import render, redirect, get_object_or_404
from .models import ProfilePage, Post
from .forms import RegistrationForm, DropPost, PostFormSet, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def index_render(request):
    posts = Post.objects.all()
    profile = ProfilePage.objects.filter(username = request.user.username)
    context = {
        'posts': posts,
        'profile': profile
 
    }

    return render(request,'main.html', context)

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            profile = ProfilePage(username=str(user.username), avatar = 'media/user_avatar/default_avatar.png')
            profile.save()

            return redirect('main')
    else:
        form = RegistrationForm()

    data = {
        'form': form,
    }
            
    return render(request, 'register.html', data)

def profile_view(request):
    profile = ProfilePage.objects.filter(username = request.user.username)
    username = request.user.username
    context = {
        'profile': profile,
        'username': username,
    }
    return render(request, 'profile.html', context)

def post_view(request, post_id):
   post = get_object_or_404(Post, id=post_id)
   profile = ProfilePage.objects.get(username=request.user.username)

   context = {
        'post': post,
        'profile': profile,
    }
   return render(request, 'post.html', context)

@login_required
def drop_post(request):
    if request.method == 'POST':
        form = DropPost(request.POST)
        formset = PostFormSet(request.POST)
        if form.is_valid and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            formset.instance = post
            formset.save()
            return redirect('main')
        else:
            messages.warning(request, 'form is not valid')
            return render(request, 'drop_post.html', {"form": form})

    else:

        context = {
            'form': DropPost(),
            'formset': PostFormSet()
        }
        return render(request, 'drop_post.html', context)




@login_required
def save_post(request,post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.saved_by.all():
        post.saved_by.remove(request.user) # если сохранен то убираем

    else:
        post.saved_by.add(request.user) # в противном случае добавляем

    return redirect('post', post_id = post.id)

@login_required
def saved_posts_view(request):
    user = request.user
    posts = user.saved_posts.all() # все посты, которые пользователь сохранил

    context = {
        'posts': posts,
    }
    return render(request, 'post_saved.html', context)

    
def login_render(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:   # ← ВАЖНО
                login(request, user)
                return redirect('main')
            else:
                form.add_error(None, "Неверный логин или пароль")

    return render(request, 'login.html', {'form': form})

def profile_edit(request):
    return render(request, 'profile_edit.html')

    


    
    














    

