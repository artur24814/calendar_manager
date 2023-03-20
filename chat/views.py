from django.shortcuts import render
from django.shortcuts import get_object_or_404

from chat.models import Room, Message, UnreadMessage
from django.contrib.auth.models import User


def index_view(request):
    return render(request, 'chat/index.html', {
        'rooms': Room.objects.all(),
        'unread_msgs': UnreadMessage.objects.filter(user=request.user)
    })

def open_room_view(request, room_name):
    chat_room, created = Room.objects.get_or_create(name=room_name)
    room_messages = Message.objects.filter(room=chat_room).order_by('timestamp')
    return render(request, 'chat/room.html', {
        'room': chat_room,
        'room_messages': room_messages
    })


def create_room_view(request, username):
    variant_1 = Room.objects.filter(name=f'{request.user.username}_{username}').first()
    variant_2 = Room.objects.filter(name=f'{username}_{request.user.username}').first()
    oposite_user = get_object_or_404(User,username=username)
    if variant_1:
        chat_room = Room.objects.get(name=f'{request.user.username}_{username}')
    elif variant_2:
        chat_room = Room.objects.get(name=f'{username}_{request.user.username}')
    elif variant_1 is None and variant_2 is None:
        chat_room = Room.objects.create(name=f'{request.user.username}_{username}')
        chat_room.users.add(request.user)
        chat_room.users.add(oposite_user)
    room_messages = Message.objects.filter(room=chat_room).order_by('timestamp')
    return render(request, 'chat/room.html', {
        'room': chat_room,
        'room_messages': room_messages
    })

