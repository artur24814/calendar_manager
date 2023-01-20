from .models import Meetings

def navbar_messages(request):
    """
    context processor to check unread message and show it to user wherever user is in website,
    """
    unconfirmed_meeetins = Meetings.objects.filter(replied=request.user.pk, confirmed=False)
    return {'quantity_meetings': len(unconfirmed_meeetins)}