from django.urls import path

from .views import (
    CalendarView, TimelineForFollowers, AcceptMeeting, infoTimeline, ListUsersView
)

app_name = 'calendar'

urlpatterns = [
    path('users/', ListUsersView.as_view(), name='users'),
    path('calendar/<user_pk>/', CalendarView.as_view(), name='calendar'),
    path('info-timeline/', infoTimeline, name='info-timeline'),
    path('timeline-for-followers/<int:month>/<int:day>/<int:user_pk>/', TimelineForFollowers.as_view(), name='timeline-followers'),
    path('meetings/accept/<int:pk_meeting>/', AcceptMeeting.as_view(), name='meeting-accept'),
    #Duplicate url without argunments (for adding variables to JS)
    path('meetings/accept/', CalendarView.as_view(), name='meeting-accept-no-args'),
    path('calendar/', CalendarView.as_view(), name='calendar-no-args'),

]