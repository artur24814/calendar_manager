import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
import datetime
from django.contrib.messages import get_messages
from calendar_manager.models import Day, Meetings

now = datetime.datetime.now()


@pytest.mark.django_db
def test_calendar_get(client, user, in_memory, login_user):
    response = client.get(reverse('calendar:calendar', kwargs={'user_pk': user.id}))

    assert response.status_code == 200
    assertTemplateUsed(response, 'calendar_manager/calendar.html')

"****Timeline****"
@pytest.mark.django_db
def test_logout_user(client, user, in_memory):
    client.logout()
    response = client.post(reverse('calendar:timeline-followers', 
                                   kwargs={'month': now.month,'day': now.day,'user_pk': user.id}),  
                                   data={'time_start': now.strftime('%H:%M'), 'title':'Test', 'message': 'test_message'})
    
    assert response.status_code == 302
    assert response['Location'] == f'/login/?next=/calendar/timeline-for-followers/{now.month}/{now.day}/{user.id}/'

@pytest.mark.django_db
def test_ask_form(client, user, user2, in_memory, login_user):
    response = client.post(reverse('calendar:timeline-followers', 
                                   kwargs={'month': now.month,'day': now.day,'user_pk': user2.id}),  
                                   data={'time_start': now.strftime('%H:%M'), 'title':'Test', 'message': 'test_message'})
    day = Day.objects.all()
    meeting = Meetings.objects.all()
    
    assert response.status_code == 302
    assert response['Location'] == reverse('calendar:calendar', kwargs={'user_pk': user2.id})
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == 'Your request for meeting was send, wait for confirm'

    assert len(day) == 2
    assert len(meeting) == 1

    assert meeting.first().asker == user
    assert meeting.first().replied == user2
    assert meeting.first().confirmed == False

@pytest.mark.django_db
def test_ask_form_error(client, user, in_memory, login_user):
    response = client.post(reverse('calendar:timeline-followers', 
                                   kwargs={'month': now.month,'day': now.day,'user_pk': user.id}),  
                                   data={'time_start': 'errorr13:56.p.m', 'title':'Test', 'message': 'test_message'})
    
    assert response.status_code == 302
    assert response['Location'] == reverse('calendar:calendar', kwargs={'user_pk': user.id})
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == 'Upss, correct ask form and try again'

'*******Meetings*******'
@pytest.mark.django_db
def test_logout_user_in_meeting(client, user, user2, in_memory, login_user):
    response = client.post(reverse('calendar:timeline-followers', 
                                   kwargs={'month': now.month,'day': now.day,'user_pk': user2.id}),  
                                   data={'time_start': now.strftime('%H:%M'), 'title':'Test', 'message': 'test_message'})
    assert len(Day.objects.all()) == 2
    assert len(Meetings.objects.all()) == 1

    client.logout()
    response2 = client.post(reverse('calendar:meeting-accept', 
                                   kwargs={'pk_meeting': Meetings.objects.all().first().id}))
    
    assert response2.status_code == 302
    assert response2['Location'] == f'/login/?next=/calendar/meetings/accept/{Meetings.objects.all().first().id}/'

@pytest.mark.django_db
def test_accept_meeting(client, user, user2, in_memory):
    #The logged in user invites user 2 to a meeting.
    client.force_login(user)
    response = client.post(reverse('calendar:timeline-followers', 
                                   kwargs={'month': now.month,'day': now.day,'user_pk': user2.id}),  
                                   data={'time_start': now.strftime('%H:%M'), 'title':'Test', 'message': 'test_message'})
    days = Day.objects.all()
    for day in days:
        day.available_places = 7
        day.save()
    assert len(days) == 2
    assert len(Meetings.objects.all()) == 1
    assert Meetings.objects.all().first().asker == user
    assert Meetings.objects.all().first().replied == user2
    assert Meetings.objects.all().first().confirmed == False

    #Logged in user2 accepts this meeting
    #++++++++++++++++++++++++++++++++++++
    client.logout()
    client.force_login(user2)

    response2 = client.get(reverse('calendar:meeting-accept', 
                                   kwargs={'pk_meeting': Meetings.objects.all().first().id}))
    
    assert response2.status_code == 302
    assert response2['Location'] == reverse('calendar:calendar', kwargs={'user_pk': user2.id})
    assert Meetings.objects.all().first().confirmed is True

    days = Day.objects.all()
    for day in days:
        assert day.count_meetings == 1
        assert day.available_places == 6