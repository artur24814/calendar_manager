from .models import Meetings
from django.contrib.auth.models import User
from .utils import now
from django.forms.models import model_to_dict
import json
from django.core.serializers.json import DjangoJSONEncoder
from chat.models import Room

def navbar_messages(request):
    """
    context processor to check unread message and show it to user wherever user is in website,
    """
    try:
        all_user_chat_room = request.user.rooms.all()
        unconfirmed_meeetins = Meetings.objects.filter(replied=request.user.pk, confirmed=False)
        all_meetings = Meetings.objects.filter(replied=request.user) | Meetings.objects.filter(asker=request.user)
        list_meetings = [model_to_dict(meeting) for meeting in all_meetings.filter(date__gte=now).order_by('-time_start').order_by('date')]
        dict_meetings = {}
        for element in list_meetings:
            dict_meetings[f'{list_meetings.index(element)}'] = element
            asker = User.objects.get(pk=int(element['asker']))
            dict_meetings[f'{list_meetings.index(element)}']['asker'] = { 
                'name': asker.first_name + ' ' + asker.last_name,
                'img_url': asker.profile.image.url
                }
            replied = User.objects.get(pk=int(element['replied']))
            dict_meetings[f'{list_meetings.index(element)}']['replied'] = { 
                'name': replied.first_name + ' ' + replied.last_name,
                'id': replied.id,
                'img_url': replied.profile.image.url
                }
            # dict_meetings[f'{list_meetings.index(element)}']['replied'] = model_to_dict(element.replied.profile)
        return {'quantity_meetings': len(unconfirmed_meeetins), 
                'all_meetings': json.dumps(dict_meetings, sort_keys=True, indent=1, cls=DjangoJSONEncoder),
                'rooms': all_user_chat_room}
    except:
        return {'quantity_meetings': '', 'all_meetings': '', 'rooms': ''}