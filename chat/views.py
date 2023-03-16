from django.shortcuts import render

from chat.models import Room, Message


def index_view(request):
    return render(request, 'chat/index.html', {
        'rooms': Room.objects.all(),
    })


def room_view(request, room_name):
    changed_room_name = room_name + '-' + request.user.username
    chat_room, created = Room.objects.get_or_create(name=changed_room_name)
    room_messages = Message.objects.filter(room=chat_room).order_by('timestamp')
    return render(request, 'chat/room.html', {
        'room': chat_room,
        'room_messages': room_messages
    })
