from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .forms import UserForm, SettingsForm
from .models import Picture
from functools import wraps
import re
import os


# Regular Expressions
UNAME_RE = re.compile(r'^[0-9a-zA-z_-]+$')
EMAIL_RE = re.compile(r'^[0-9a-zA-z_-]+@[a-zA-Z0-9]([a-zA-Z0-9-]*\.)+[a-z]{2,}$')


# Session check decorators
def verified(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        else:
            return redirect('Profile:index')
    return inner


def notverified(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return func(request, *args, **kwargs)
        else:
            return redirect('Profile:index')
    return inner


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'Profile/home.html', {'title': 'Complec City'})
    return render(request, 'Profile/profile.html')


@notverified
def register(request):
    if request.method == 'POST':
        post = request.POST

        # Check form fields
        context = invalid_data(post)
        if context:
            return render(request, 'Profile/register.html', context)

        # Create user and redirect to Profile
        return create_user(request, post)

    return render(request, 'Profile/register.html', {'title': 'Register an account'})


def invalid_data(post):
    context = {'title': 'Register an account'}
    # fields
    username = UNAME_RE.match(post.get('username'))
    email = EMAIL_RE.match(post.get('email'))
    password = post.get('password')
    confirm = post.get('confirmpass')

    flag = False

    if username:
        try:
            username = username.group()
            User.objects.get(username=username)
            flag = True
            context['invalid_user'] = 'Username is already registered'
        except ObjectDoesNotExist:
            context['username'] = username
    else:
        flag = True
        context['invalid_user'] = 'Invaled username'

    if email:
        try:
            email = email.group()
            User.objects.get(email=email)
            flag = True
            context['invalid_email'] = 'Email is already registered'
        except ObjectDoesNotExist:
            context['email'] = email
    else:
        flag = True
        context['invalid_email'] = 'Invaled email'

    if len(password) < 8:
        flag = True
        context['shortpassword'] = True

    if password != confirm:
        flag = True
        context['missmatch'] = True

    if flag:
        return context
    return False


def create_user(request, post):
    form = UserForm(post)
    if form.is_valid():
        user = form.save(commit=False)

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user.set_password(password)

        user.save()

        user = authenticate(username=username, password=password)

        if user and user.is_active:
            login(request, user)
            return redirect('Profile:index')
    return render(request, 'Profile/register.html', {'title': 'Register an account'})


@notverified
def log_in(request):
    context = {'title': 'Log in'}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        ip = request.META.get('REMOTE_ADDR')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('Profile:index')
            else:
                context['message'] = 'Account is disabled.'
        else:
            context['message'] = 'Invalid username or password.'
            context['username'] = username

    return render(request, 'Profile/login.html', context)


@verified
def log_out(request):
    logout(request)
    return redirect('Profile:index')


@verified
def settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            image = form.cleaned_data['image']

            user = request.user

            if first_name:
                user.first_name = first_name.lower().capitalize()
            if last_name:
                user.last_name = last_name.lower().capitalize()
            if image:
                fname = 'media/' + user.username + os.path.splitext(image.name)[1]
                save_image(fname, image)

                try:
                    picture = user.picture
                except ObjectDoesNotExist:
                    user.picture = Picture(user=user)
                    picture = user.picture

                picture.image = fname
                picture.save()

            user.save()
            return redirect('Profile:index')
    else:
        form = SettingsForm()

    return render(request, 'Profile/settings.html', {'form': form})


def save_image(name, f):
    with open(name, 'wb') as fp:
        for chunk in f.chunks():
            fp.write(chunk)
