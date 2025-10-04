from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import MasterRegistrationForm, MasterLoginForm
from .models import Master
from django.core.cache import cache
from django.http import HttpResponseForbidden


def rate_limit(key, limit=5, timeout=60):
    count = cache.get(key, 0)
    if count >= limit:
        return True
    cache.set(key, count + 1, timeout)
    return False

def register(request):
    if request.method == 'POST':
        form = MasterRegistrationForm(request.POST)
        if form.is_valid():
            master = form.save(commit=False)
            master.set_password(form.cleaned_data['password'])
            master.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('master:login')
    else:
        form = MasterRegistrationForm()

    return render(request, 'master/register.html', {'form': form})


def login(request):
    ip = request.META.get('REMOTE_ADDR')

    if rate_limit(f'login_attempt_{ip}'):
        messages.error(request, 'Too many login attempts. Please try again later.')
        return render(request, 'master/login.html')

    if request.method == 'POST':
        form = MasterLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                master = Master.objects.get(username=username, is_active=True)
                if master.check_password(password):
                    request.session['master_id'] = master.id
                    request.session['master_username'] = master.username
                    return redirect('dashboard:dashboard')
                else:
                    messages.error(request, 'Invalid credentials')
            except Master.DoesNotExist:
                messages.error(request, 'Invalid credentials')
    else:
        form = MasterLoginForm()

    return render(request, 'master/login.html', {'form': form})


def logout(request):
    if 'master_id' in request.session:
        del request.session['master_id']
        del request.session['master_username']
    messages.success(request, 'You have been logged out successfully.')
    return redirect('master:login')


def master_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'master_id' not in request.session:
            messages.error(request, 'Please login to access this page.')
            return redirect('master:login')
        return view_func(request, *args, **kwargs)

    return wrapper
