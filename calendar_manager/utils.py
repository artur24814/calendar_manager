'''
Helper functions
'''
from .models import Day, Meetings
from django.utils.timezone import get_current_timezone
from datetime import timedelta
import datetime



now = datetime.datetime.now(tz=get_current_timezone())

def add_day_model(user, month, day):
    day_model, created = Day.objects.get_or_create(owner=user,
                                year=now.year,
                                month=month,
                                day=day,
    )
    if created is True:
        day_model.available_places=user.profile.day_available_places
        day_model.save()
    return day_model
