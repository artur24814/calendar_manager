from django.shortcuts import render, redirect, get_object_or_404
import calendar
import datetime
from django.urls import reverse
from django.utils.timezone import get_current_timezone
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AskMeetingsForm
from .models import Day, Meetings
from datetime import timedelta
from django.contrib import messages
from django.utils.translation import gettext as _

from .utils import now, add_day_model



class HomePageView(View):
    """
    Home page
    """
    def get(self, request):
        context = {}
        return render(request, 'home/homepage.html', context)

# class MyCalendarView(LoginRequiredMixin,View):
#     month2 = calendar.monthcalendar(now.year, now.month)
#     today = now.day
#     year = now.year
#     month_name = calendar.month_name[now.month]
#     month = now.month

#     def get(self, request):
#         user = request.user
#         days = Day.objects.filter(owner=request.user).filter(month=self.month).filter(year=self.year)

#         context = {
#             'days': days,
#             'user': user,
#             'today': self.today,
#             'month2': self.month2,
#             'month': self.month,
#             'year': self.year,
#             'month_name': self.month_name
#         }
#         return render(request, 'calendar_manager/calendar.html', context)

class CalendarView(View):
    """
    Calendar View

    :in:
        Calendar with actual date
        :model: user

    :return:
        template `calendar.html`
    """
    month2 = calendar.monthcalendar(now.year, now.month)
    today = now.day
    year = now.year
    month_name = calendar.month_name[now.month]
    month = now.month
    def get(self, request, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        days = Day.objects.filter(owner=user, month=self.month, year=self.year)
        context = {
            'days': days,
            'user': user,
            'today': self.today,
            'month2': self.month2,
            'month': self.month,
            'year': self.year,
            'month_name': self.month_name
        }
        return render(request, 'calendar_manager/calendar.html', context)


class Timeline(View):
    """
    Timeline for login User

    :in:
        month, day
    :return:
        Queryset :model:Meetings
        Template `timeline.html`
    """
    def get(self, request, month, day):
        month_name = calendar.month_name[month]
        try:
            day = Day.objects.get(month=month, day=day, owner=request.user)
            meetings = day.meeting.all().order_by('time_start')
        except Exception:
            meetings = []
        context = {
            'meetings': meetings,
            'month': month_name,
            'day': day,
        }
        return render(request, 'calendar_manager/timeline.html', context)


class TimelineForFollowers(View):
    """
    Timeline for Users

    :in:
        month, day, user_pk
    **GET**
    :return:
        :form: `AskMeetingsForm`
        Queryset :model:Meetings
        Template `timeline_for_followers.html`
    **POST**
    :return:
        create :model:Day for request.user and user.user_pk
                :model:Meeting 
                add :model:Meeting to :model:Day
        Template `timeline_for_followers.html`
    """
    def get(self, request, month, day, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        if user == request.user:
            return redirect(reverse('calendar:timeline', kwargs={'month': month, 'day': day}))
        month_name = calendar.month_name[month]
        form = AskMeetingsForm()
        try:
            day = Day.objects.get(month=month, day=day, owner=user)
            meetings = day.meeting.all().order_by('time_start')
        except Exception:
            meetings = {}
        context = {
            'user': user,
            'form': form,
            'meetings': meetings,
            'month': month_name,
            'day': day,
        }
        return render(request, 'calendar_manager/timeline_for_followers.html', context)

    def post(self, request, month, day, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        form = AskMeetingsForm(request.POST)
        if form.is_valid():
            #count time finish
            time_finish = datetime.datetime.combine(datetime.date.today(), form.cleaned_data['time_start']) + timedelta(minutes=30)
            meeting = form.save(commit=False)
            meeting.asker = request.user
            meeting.replied = user
            meeting.time_finish = time_finish.time()
            meeting.date = datetime.datetime(datetime.datetime.now().year, month, day)
            meeting.save()
            #create or get days for user and oponents
            day_user = add_day_model(request.user, month, day)
            day_opponent_users = add_day_model(user, month, day)
            #add meeting for both users
            day_user.meeting.add(meeting)
            day_opponent_users.meeting.add(meeting)
            
            messages.success(request, _('Your request for meeting was send, wait for confirm'))
            return redirect(reverse('calendar:timeline-followers', kwargs={'month': month, 'day': day, 'user_pk': user_pk}))
        meetings = Meetings.objects.all()
        month = calendar.month_name[month]
        context = {
            'user': user,
            'form': form,
            'meetings': meetings,
            'month': month,
            'day': day,
        }
        return render(request, 'calendar_manager/timeline_for_followers.html', context)

class MeetingsListView(View):
    """
    Meetings List View

    :return:
        Queryset :model:Meetings for request.user
    """
    def get(self,request):
        all_meetings = Meetings.objects.filter(replied=request.user) | Meetings.objects.filter(asker=request.user)
        context = {
            'user': request.user,
            'meetings': all_meetings.filter(date__gte=now).order_by('-time_start').order_by('date')
        }
        return render(request, 'calendar_manager/meetings_list.html', context)

class AcceptMeeting(View):
    """
    Accept meeting requirement

    :in:
        pk_meeting
    :return:
        :model:Meeting.acept is True
        set of :model:Day.count meeting + 1
        redirect `meetings-list`
    """
    def get(self, request, pk_meeting):
        meeting = get_object_or_404(Meetings, pk=pk_meeting)
        if meeting.replied == request.user and meeting.confirmed is False:
            days = meeting.days.all()
            for day in days:
                if day.available_places == 0:
                    messages.success("You or oponent haven't available plases on this day please, please change a day meeting")
                    return redirect(reverse('calendar:meetings-list'))
                day.count_meetings += 1
                day.available_places -= 1
                day.save()
            meeting.confirmed = True
            meeting.save()
        return redirect(reverse('calendar:meetings-list'))



