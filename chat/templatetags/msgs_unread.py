from django import template
from chat.models import UnreadMessage

register = template.Library()

@register.filter(name='unread')
def unread(value, user):
    return len(UnreadMessage.objects.filter(room=value, user=user))

@register.filter(name='unread_all')
def unread_all(user):
    return len(UnreadMessage.objects.filter(user=user))

@register.filter(name='unread_last')
def unread_last(user):
    msg_obj = UnreadMessage.objects.filter(user=user).order_by('-message__timestamp')[0]
    return msg_obj.message.content