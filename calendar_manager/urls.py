from django.urls import path

from .views import (
    CalendarView, TimelineView, AcceptMeeting, infoTimeline, ListUsersView, folowUnfolowView, ListFriendsView
)

app_name = 'calendar'

urlpatterns = [
    path('users/', ListUsersView.as_view(), name='users'),
    path('friends/', ListFriendsView.as_view(), name='friends'),
    path('calendar/<user_pk>/', CalendarView.as_view(), name='calendar'),
    path('info-timeline/', infoTimeline, name='info-timeline'),
    path('timeline-for-followers/<int:month>/<int:day>/<int:user_pk>/', TimelineView.as_view(), name='timeline-followers'),
    path('meetings/accept/<int:pk_meeting>/', AcceptMeeting.as_view(), name='meeting-accept'),
    path('follow/<int:profile_pk>/', folowUnfolowView, name='follow'),
    #Duplicate url without argunments (for adding variables to JS)
    path('meetings/accept/', CalendarView.as_view(), name='meeting-accept-no-args'),
    path('calendar/', CalendarView.as_view(), name='calendar-no-args'),

]