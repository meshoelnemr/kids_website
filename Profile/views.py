from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .forms import UserForm
from functools import wraps
import re


UNAME_RE = re.compile(r'[0-9a-zA-z_]+')
EMAIL_RE = re.compile(r'[0-9a-zA-z_-]+@[0-9a-zA-z_-]+')


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
        print(request.META.get('REMOTE_ADDR'))
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

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('Profile:index')
            else:
                context['message'] = 'Account is disabled.'
        else:
            context['message'] = 'Invalid username or password.'
    return render(request, 'Profile/login.html', context)


@verified
def log_out(request):
    logout(request)
    return redirect('Profile:index')

