from django.urls import path

from .views import (
    CalendarView, Timeline, TimelineForFollowers, MeetingsListView, AcceptMeeting
)

app_name = 'calendar'

urlpatterns = [
    # path('my-calendar/', MyCalendarView.as_view(), name='my-calendar'),
    path('calendar/<user_pk>/', CalendarView.as_view(), name='calendar'),
    path('timeline/<int:month>/<int:day>/', Timeline.as_view(), name='timeline'),
    path('timeline-for-followers/<int:month>/<int:day>/<int:user_pk>/', TimelineForFollowers.as_view(), name='timeline-followers'),
    path('meetings', MeetingsListView.as_view(), name='meetings-list'),
    path('meetings/accept/<int:pk_meeting>/', AcceptMeeting.as_view(), name='meeting-accept'),
]