from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from functools import wraps


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
        return render(request, 'Profile/register.html', {'title': 'Register a new account'})
    return render(request, 'Profile/index.html')


@notverified
def register(request):
    form = UserForm(request.POST)
    context = {'title': 'Register a new account'}

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

    if request.method == 'POST':
        context['error'] = 'Operation failed!'

    return render(request, 'Profile/register.html', context)


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
                context['error'] = 'Account is disabled!'
        else:
            context['error'] = 'Login Failed!'
    return render(request, 'Profile/login.html', context)


@verified
def log_out(request):
    logout(request)
    return redirect('Profile:index')

