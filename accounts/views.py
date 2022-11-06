from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .forms import SignUpForm, ProfileForm


class RegisterView(View):
    """
    view for creating new user
    """
    def get(self, request):
        form = SignUpForm()
        context = {
            'form': form
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request):
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, _('Account stworzony'))
            return redirect(reverse('accounts:profile', kwargs={'user_pk': user.pk}))
        else:
            return render(request, 'accounts/register.html', {'form': form})

class ProfileView(View):
    def get(self, request, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        form = ProfileForm()
        context = {
            'user': user,
            'form': form,
        }
        return render(request, 'accounts/profile.html', context)

    def post(self, request, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            add_owner = form.save(commit=False)
            add_owner.owner = user
            add_owner.save()
            return redirect(reverse('accounts:login'))
        context = {
            'user': user,
            'form': form,
        }
        return render(request, 'accounts/profile.html', context)

class LoginView(View):
    """
    login view
    """
    def get(self, request):
        form = AuthenticationForm(request)
        context = {
            'form': form
        }
        return render(request, 'accounts/login.html', context)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('/crf/patient/')
        context = {
            'form': form
        }
        return render(request, 'accounts/login.html', context)


class LogoutView(View):
    """
    logout view
    """
    def post(self, request):
        logout(request)
        return redirect('/login/')
