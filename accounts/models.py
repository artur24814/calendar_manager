from django.db import models
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
import datetime
from django.utils.timezone import get_current_timezone
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from core.settings import STATICFILES_DIRS


ROLE = [
    ('0', 'Organisation'),
    ('1', 'Own business'),
    ('2', 'User')
]
WORK_REG = [
    (1, 'Mon-Fri'),
    (2, 'Mon-Sun'),
    (3, 'Mon-Sat'),
    (4, 'Sun-Sat'),
]
MEETING_TYPE = [
    (15, '15m'),
    (30, '30m'),
    (45, '45m'),
    (60, '1h'),
    (1, '1d'),
]
CALENDAR_SCOPE = [
    (0, 'all'),
    (1, 'only friends'),
    (2, 'only me'),
]

#User profile model
class Profile(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="images/", default='images/default.jpg')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=ROLE, null=True)
    work_regulations = models.IntegerField(choices=WORK_REG, default=1, null=True)
    available_from = models.TimeField(blank=True, null=True)
    available_to = models.TimeField(blank=True, null=True)
    meeting_type = models.IntegerField(choices=MEETING_TYPE, default=2, null=True)
    birthday = models.DateField(null=True)
    age = models.IntegerField(null=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    adress = models.TextField(null=True, blank=True)
    calendar_scope = models.IntegerField(choices=CALENDAR_SCOPE, null=True)
    day_available_places = models.IntegerField(null=True)
    facebook = models.URLField(max_length=400, null=True, blank=True)
    github = models.URLField(max_length=400, null=True, blank=True)
    twitter = models.URLField(max_length=400, null=True, blank=True)
    instagram = models.URLField(max_length=400, null=True, blank=True)
    website = models.URLField(max_length=400, null=True, blank=True)

    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)

    #for Organizations
    employee = models.ManyToManyField('Employee', related_name='company', blank=True)
    posts = models.ManyToManyField('Posts', related_name='company_post', blank=True)

    class Meta:
        permissions = (
            ("add_employee", "can add employee"),
            )


    def save(self, *args, **kwargs):
        try:
            today = datetime.datetime.now(tz=get_current_timezone()).today()
            self.age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
            #count every day available places
            #substract finish work and start work
            result = datetime.datetime.combine(datetime.date.today(),self.available_to) - datetime.datetime.combine(datetime.date.today(),self.available_from)
            if self.meeting_type == 0:
                self.day_available_places = 1 #for full day meeting
            else:
                #divide working day by type of meeting
                self.day_available_places = int(result.seconds/(self.meeting_type*60))

            if self.role == '0':
                employer_group, created = Group.objects.get_or_create(name="Employer")
                permission = Permission.objects.get(name='add_employee')
                employer_group.permissions.add(permission)
                self.owner.groups.add(employer_group)
            super().save(*args, **kwargs)
        except Exception as e:
            print(e)
            super().save(*args, **kwargs)
    def __str__(self):
        return self.owner.first_name + " " + self.owner.last_name
    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=500, null=True)
    responsibilities = models.TextField(null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Posts(models.Model):
    title = models.CharField(max_length=500)
    descriptions = models.TextField()
    date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title 

#Create Profile when new User Signs Up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(owner=instance)
        user_profile.save()
        #User follow themselves
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(create_profile, sender=User)

