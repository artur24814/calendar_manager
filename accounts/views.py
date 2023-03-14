from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .forms import SignUpForm, ProfileForm
from .validators import validate_password


class RegisterView(View):
    """
    View for creating new user
    :out:
        :model: `User`
        :model: `Profile`
        login user
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
            #save user
            user = form.save()
            messages.info(request, _("Thanks for registering. You are now logged in."))
            #sigh in user
            user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, user)
            return redirect(reverse('accounts:profile', kwargs={'user_pk': user.pk}))
        else:
            return render(request, 'accounts/register.html', {'form': form})

class ProfileView(View):
    '''
    Profile updating view 
    '''
    def get(self, request, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        form = ProfileForm(instance=user.profile)
        context = {
            'user': user,
            'form': form,
        }
        return render(request, 'accounts/profile.html', context)

    def post(self, request, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        form = ProfileForm(request.POST, request.FILES , instance=user.profile)
        if form.is_valid():
            add_owner = form.save(commit=False)
            add_owner.save()
            return redirect(reverse('home'))
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
            return redirect(reverse('home'))
        context = {
            'form': form
        }
        return render(request, 'accounts/login.html', context)


class LogoutView(View):
    """
    logout view
    """
    def get(self, request):
        logout(request)
        return redirect('/login/')

"""

HTMX views
views for HTMX method. Doesn't screen in template only for work with HTMX

"""
def valid_password(request):
    name = request.POST.get('username')
    password = request.POST.get('password1')
    if password is None:
        return HttpResponse('')
    result = validate_password(password)
    if name.upper() in password.upper() and name != '':
        return HttpResponse('nie może być zbyt podobne do innych Twoich danych osobowych')
    return HttpResponse(f'{result}')

def check_existing_name(request):
    name = request.GET.get('username')
    user = User.objects.filter(username=name).first()
    if user:
        return HttpResponse('Taki login już istnieje')
    return HttpResponse('')
