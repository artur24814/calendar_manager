from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
import datetime
from django.utils.timezone import get_current_timezone

#for translation
from django.utils.translation import gettext_lazy as _


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    class Meta(UserCreationForm.Meta):
        model = User
        # fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['age', 'owner']
        widgets = {
            'birthday': forms.DateInput(format=('%Y-%m-%d'),
                                          attrs={'class': 'form-control',
                                                 'type': 'date'}),
            'available_from': forms.TimeInput(format=('%H:%M'),
                                        attrs={'class': 'form-control',
                                               'type': 'time'}),
            'available_to': forms.TimeInput(format=('%H:%M'),
                                              attrs={'class': 'form-control',
                                                     'type': 'time'}),
        }