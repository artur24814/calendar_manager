from django.urls import path

from .views import (
    CalendarView, TimelineView, AcceptMeeting, infoTimeline, ListUsersView, folowUnfolowView, 
    ListFriendsView, add_employer_view, change_emploee_view, create_post_view, delete_post_view, PostDetailView
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
    path('add-employer/<int:user_pk>/', add_employer_view, name='add-employer'),
    path('change-employee/<int:employee_pk>/', change_emploee_view, name='change-employee'),
    path('create-post/', create_post_view, name='create-post'),
    path('delete-post/<int:id_post>/', delete_post_view, name='delete-post'),
    path('post-detail/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    #Duplicate url without argunments (for adding variables to JS)
    path('meetings/accept/', CalendarView.as_view(), name='meeting-accept-no-args'),
    path('calendar/', CalendarView.as_view(), name='calendar-no-args'),
]