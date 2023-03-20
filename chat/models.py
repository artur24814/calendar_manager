from django.contrib.auth.models import User
from django.db import models

from django.db.models.signals import post_save


class Room(models.Model):
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=User, blank=True)
    users = models.ManyToManyField(to=User, related_name='rooms', blank=True)
    

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'


class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'
    
class UnreadMessage(models.Model):
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    message = models.ForeignKey(to=Message, on_delete=models.CASCADE, null=True)

#create unread messages for offline users
def create_unread_message(sender, instance, created, **kwargs):
    if created:
        #if all users are online
        # unread message not created, clean all unread messages
        if len(instance.room.users.all()) == len(instance.room.online.all()):
            unread_msgs = UnreadMessage.objects.filter(room=instance.room)
            for msg in unread_msgs:
                msg.delete()
        else:
            for user in instance.room.users.all():
                # create unread messages for all offline users
                if user not in instance.room.online.all():
                    objects_msg = UnreadMessage.objects.create(room=instance.room, user=user, message=instance)
                #delete all unread messages for all online users
                else:
                    UnreadMessage.objects.filter(room=instance.room, user=user).delete()

post_save.connect(create_unread_message, sender=Message)
