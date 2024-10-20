from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                safe_home = reverse_lazy('cinema:index')
                # Sprawdź, czy przekierowanie jest bezpieczne
                redirect_to = request.POST.get('next', safe_home)
                if not url_has_allowed_host_and_scheme(url=redirect_to, allowed_hosts={request.get_host()}):
                    redirect_to = safe_home
                return redirect(redirect_to)
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)  # Wylogowanie użytkownika
    return redirect(reverse_lazy('cinema:index'))  # Przekierowanie na wybraną stronę


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Logowanie użytkownika po rejestracji
            return redirect(reverse_lazy('cinema:index'))  # Przekierowanie po rejestracji
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})