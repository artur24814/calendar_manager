from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required

from chat.models import Room, Message, UnreadMessage

@login_required
def index_view(request):
    return render(request, 'chat/index.html')

@login_required
# open existing room
def open_room_view(request, room_name):
    chat_room, created = Room.objects.get_or_create(name=room_name)
    room_messages = Message.objects.filter(room=chat_room).order_by('timestamp')
    return render(request, 'chat/room.html', {
        'room': chat_room,
        'room_messages': room_messages
    })

@login_required
# create or get room
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

@login_required
@permission_required("accounts.add_employee")
#create group chat
def create_group_company_chat(request):
    chat_room, created = Room.objects.get_or_create(name=f'{request.user.username}_incorporated')
    #add employees to the chat
    for user in request.user.profile.employee.all():
        #add user if chat just created
        if created:
            chat_room.users.add(request.user)
        if user not in chat_room.users.all():
            chat_room.users.add(user.user)
    return redirect(reverse('chat:chat-room', kwargs={'room_name': chat_room.name}))   

