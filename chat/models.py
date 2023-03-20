from django.contrib.auth.models import User
from django.db import models


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

    def save(self, *args, **kwargs):
        if len(self.room.users.all()) == len(self.room.online.all()):
            unread_msgs = UnreadMessage.objects.filter(room=self.room)
            for msg in unread_msgs:
                msg.delete()
        else:
            for user in self.room.users.all():
                if user not in self.room.online.all():
                    UnreadMessage.objects.create(room=self.room, user=user)
        super(Message, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'
    
class UnreadMessage(models.Model):
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
