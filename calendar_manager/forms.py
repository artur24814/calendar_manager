from django import forms
from .models import Meetings


class AskMeetingsForm(forms.ModelForm):
    class Meta:
        model = Meetings
        fields = ['time_start','title', 'message']

        widgets = {
            'time_start': forms.TimeInput(format=('%H:%M'), attrs={'class': 'form-control', 'type': 'time'})}

