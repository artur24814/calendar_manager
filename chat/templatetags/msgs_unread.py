from django import template
from chat.models import UnreadMessage

register = template.Library()

@register.filter(name='unread')
def unread(value, user):
    return len(UnreadMessage.objects.filter(room=value, user=user))

@register.filter(name='unread_all')
def unread_all(user):
    return len(UnreadMessage.objects.filter(user=user))