'''
Helper functions
'''
from .models import Day, Meetings
from django.utils.timezone import get_current_timezone
from datetime import timedelta
import datetime

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail



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


def sendHTMLEmail(request, subject, user_email):
    context ={
        "title":"Test",
        "content":"Testing sending HTML emails from Django"
    }
    html_message = render_to_string('email/info_emails.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'From <from@example.com>'
    mail.send_mail(subject, plain_message, from_email, [user_email], html_message=html_message)

    return "Email Sent successfully"