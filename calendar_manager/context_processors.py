from .models import Meetings
from .utils import now
from django.forms.models import model_to_dict

def navbar_messages(request):
    """
    context processor to check unread message and show it to user wherever user is in website,
    """
    unconfirmed_meeetins = Meetings.objects.filter(replied=request.user.pk, confirmed=False)
    all_meetings = Meetings.objects.filter(replied=request.user) | Meetings.objects.filter(asker=request.user)
    list_meetings = [model_to_dict(meeting) for meeting in all_meetings.filter(date__gte=now).order_by('-time_start').order_by('date')]
    return {'quantity_meetings': len(unconfirmed_meeetins), 'all_meetings': list_meetings}