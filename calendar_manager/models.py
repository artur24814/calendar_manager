from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import get_current_timezone

month = [(x, x) for x in range(1, 13)]

class Day(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField(choices=month)
    day = models.IntegerField()
    count_meetings = models.IntegerField(default=1)
    available_places = models.IntegerField()

    def __str__(self):
        return f"{self.owner} {self.year}/{self.month}/{self.day}"

class Meetings(models.Model):
    asker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asker')
    replied = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replied')
    day = models.ManyToManyField('Day')
    confirmed = models.BooleanField(default=False)
    time_start = models.TimeField()
    time_finish = models.TimeField()
    title = models.CharField(default='business meeting', max_length=180)
    message = models.TextField(blank=True, null=True)

