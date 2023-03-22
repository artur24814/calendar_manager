from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.forms.models import model_to_dict
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.http import JsonResponse

import json
import calendar
import datetime
from datetime import timedelta

from .forms import AskMeetingsForm
from .models import Day, Meetings
from accounts.models import Profile, Employee, Posts
from .utils import now, add_day_model



class HomePageView(View):
    """
    Home page
    """
    def get(self, request):
        context = {}
        return render(request, 'home/homepage.html', context)

class ListUsersView(ListView):
    """
    List Users view

    :search: by username, fierst_name, last_name
    """
    template_name = 'calendar_manager/list_users.html'
    paginate_by = 20

    #get context
    def get_context_data(self, **kwargs):
        context = super(ListUsersView, self).get_context_data(**kwargs)
        search = self.request.GET.get("search")
        if search:
            context['input'] = 'search=' + search
        return context
    
    #get filtered queryset
    def get_queryset(self):
        queryset = User.objects.all().order_by('-date_joined')
        if self.request.GET.get("search"):
            search = self.request.GET.get("search")
            queryset = User.objects.filter(username__contains=search).order_by('-date_joined') | User.objects.filter(first_name__contains=search).order_by('-date_joined') | User.objects.filter(last_name__contains=search).order_by('-date_joined')
        return queryset

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
    form = AskMeetingsForm()

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
            'month_name': self.month_name,
            'form': self.form,
        }
        return render(request, 'calendar_manager/calendar.html', context)


class TimelineView(LoginRequiredMixin,View):
    """
    Timeline for Users

    :in:
        month, day, user_pk
    **POST**
    :return:
        create :model:Day for request.user and user.user_pk
                :model:Meeting 
                add :model:Meeting to :model:Day
        redirect `calendar:calendar`
    """
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
            return redirect(reverse('calendar:calendar', kwargs={'user_pk': user_pk}))
        messages.error(request, _('Upss, correct ask form and try again'))
        return redirect(reverse('calendar:calendar', kwargs={'user_pk': user_pk}))


class AcceptMeeting(LoginRequiredMixin,View):
    """
    Accept meeting requirement

    :in:
        pk_meeting
    :return:
        :model:Meeting.acept is True
        set :model:Day.count meeting + 1
        redirect `calendar:calendar`
    """
    def get(self, request, pk_meeting):
        meeting = get_object_or_404(Meetings, pk=pk_meeting)
        if meeting.replied == request.user and meeting.confirmed is False:
            days = meeting.days.all()
            #check days timeline
            for day in days:
                if day.available_places == 0:
                    messages.success("You or your oponent haven't available plases on this day, please change a day meeting")
                    return redirect(reverse('calendar:calendar', kwargs={'user_pk': request.user.id}))
                
            #add meeting, subtract available places
            for day in days:
                day.count_meetings += 1
                day.available_places -= 1
                day.save()
            meeting.confirmed = True
            meeting.save()
        return redirect(reverse('calendar:calendar', kwargs={'user_pk': request.user.id}))
    

class ListFriendsView(LoginRequiredMixin,ListView):
    """
    List Users Followers view

    :search: by username, first_name, last_name
    """
    template_name = 'calendar_manager/list_friends.html'
    paginate_by = 20

    #get context
    def get_context_data(self, **kwargs):
        context = super(ListFriendsView, self).get_context_data(**kwargs)
        search = self.request.GET.get("search")
        if search:
            context['input'] = 'search=' + search
        return context
    
    #get filtered queryset
    def get_queryset(self):
        queryset = self.request.user.profile.follows.all().exclude(owner=self.request.user).order_by('owner__first_name')
        if self.request.GET.get("search"):
            search = self.request.GET.get("search")
            queryset = self.request.user.profile.follows.filter(owner__username__contains=search).exclude(owner=self.request.user).order_by('owner__first_name') | self.request.user.profile.follows.filter(owner__first_name__contains=search).exclude(owner=self.request.user).order_by('owner__first_name') | self.request.user.profile.follows.filter(owner__last_name__contains=search).exclude(owner=self.request.user).order_by('owner__first_name')
        return queryset


@login_required
#view for frontend    
def infoTimeline(request):
    data = json.loads(request.body)
    month_name = calendar.month_name[int(data['month'])]
    day=int(data['day'])

    #get user model
    user = get_object_or_404(User, pk=int(data['userId']))
    try:
        day_model = Day.objects.get(month=data['month'], day=day, owner=user)
        meetings = day_model.meeting.filter(confirmed=True).order_by('-time_start')
    except Exception:
        meetings = []

    listOfMeetings = []
    #formating objects to dict for json
    for meeting in meetings:
        meeting_dict = model_to_dict(meeting)
        meeting_dict['asker'] = {
            'name': meeting.asker.first_name + ' ' + meeting.asker.last_name,
            'id': meeting.asker.id,
            'img_url': meeting.asker.profile.image.url
            }
        meeting_dict['replied'] = {
            'name': meeting.replied.first_name + ' ' + meeting.replied.last_name,
            'id': meeting.replied.id,
            'img_url': meeting.replied.profile.image.url
        }
        listOfMeetings.append(meeting_dict)

    context = {
        'meetings':  listOfMeetings,
        'month': month_name,
        'day':  day,
    }

    #Show moore ditails if user is request user
    if user == request.user:
        context['show_detail'] = True
    return JsonResponse(context, safe=False)

@login_required
#Follow/Unfolllow
def folowUnfolowView(request, profile_pk):
    profile = Profile.objects.get(pk=profile_pk)

    if profile != request.user.profile:
        if profile in request.user.profile.follows.all():
            request.user.profile.follows.remove(profile)
        else:
            request.user.profile.follows.add(profile)

    return redirect(reverse('calendar:calendar', kwargs={'user_pk': profile.owner.pk}))

@login_required
@permission_required("accounts.add_employee")
def add_employer_view(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    employee_obj, create = Employee.objects.get_or_create(user=user)
    if employee_obj in request.user.profile.employee.all():
        request.user.profile.employee.remove(employee_obj)
    else:
        request.user.profile.employee.add(employee_obj)
    return redirect(reverse('calendar:calendar', kwargs={'user_pk': user_pk}))

@login_required
@permission_required("accounts.add_employee")
def change_emploee_view(request, employee_pk):
    if request.method == 'POST':
        emploee = get_object_or_404(Employee, pk=employee_pk)
        position = request.POST['position']
        responsibilities = request.POST['responsibilities']
        if position is not None and position != 'None':
            emploee.position = str(position)
            emploee.save()
        if responsibilities is not None and responsibilities != 'None':
            emploee.responsibilities = str(responsibilities)
            emploee.save()
    return redirect(reverse('calendar:calendar', kwargs={'user_pk': request.user.id}))

@login_required
@permission_required("accounts.add_employee")
def create_post_view(request):
    if request.method == 'POST':
        title = request.POST['title']
        descriptions = request.POST['descriptions']
        if title is not None and descriptions is not None:
            post = Posts.objects.create(title=title, descriptions=descriptions, owner=request.user)
            post.save()
            request.user.profile.posts.add(post)
    return redirect(reverse('calendar:calendar', kwargs={'user_pk': request.user.id}))

@login_required
@permission_required("accounts.add_employee")
def delete_post_view(request, id_post):
    post = get_object_or_404(Posts, id=id_post)
    if request.user == post.owner:
        post.delete()
        return JsonResponse('deleted', safe=False)
    return JsonResponse('Forbidden Error', safe=False)

class PostDetailView(DetailView):
    model = Posts
    template_name = 'calendar_manager/post_detail.html'


