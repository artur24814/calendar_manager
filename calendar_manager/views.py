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

now = datetime.datetime.now(tz=get_current_timezone())

class HomePageView(View):
    def get(self, request):
        context = {}
        return render(request, 'home/homepage.html', context)

class MyCalendarView(LoginRequiredMixin,View):
    month2 = calendar.monthcalendar(now.year, now.month)
    today = now.day
    year = now.year
    month_name = calendar.month_name[now.month]
    month = now.month

    def get(self, request):
        user = request.user
        days = Day.objects.filter(owner=request.user).filter(month=self.month).filter(year=self.year)

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

class CalendarView(View):
    month2 = calendar.monthcalendar(now.year, now.month)
    today = now.day
    year = now.year
    month_name = calendar.month_name[now.month]
    month = now.month
    def get(self, request, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        days = Day.objects.filter(owner=user).filter(month=self.month).filter(year=self.year)
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
    def get(self, request, month, day):
        month_name = calendar.month_name[month]
        meetings = Meetings.objects.filter(day__month=month).filter(day__day=day).filter(day__owner=request.user).order_by('time_start')
        context = {
            'meetings': meetings,
            'month': month_name,
            'day': day,
        }
        return render(request, 'calendar_manager/timeline.html', context)


def add_day_model(user, month, day):
    day_model, created = Day.objects.get_or_create(owner=user,
                                                          year=now.year,
                                                          month=month,
                                                          day=day,
                                                          available_places=10
                                                          )
    if created is False:
        day_model.count_meetings += 1
        day_model.save()
    return day_model

class TimelineForFollowers(View):
    def get(self, request, month, day, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        month_name = calendar.month_name[month]
        form = AskMeetingsForm()
        try:
            this_day = Day.objects.get(month=month, day=day, owner=user)
            meetings = Meetings.objects.filter(day=this_day).order_by('time_start')
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
            time_finish = datetime.datetime.combine(datetime.date.today(), form.cleaned_data['time_start']) + timedelta(minutes=30)
            form_correct = form.save(commit=False)
            form_correct.asker = request.user
            form_correct.replied = user
            form_correct.time_finish = time_finish.time()
            day_user = add_day_model(request.user, month, day)
            day_opponent_users = add_day_model(user, month, day)
            form_correct.save()
            form_correct.day.add(day_user)
            form_correct.day.add(day_opponent_users)
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

