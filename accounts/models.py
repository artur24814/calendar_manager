from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import get_current_timezone
from django.core.validators import RegexValidator


ROLE = [
    ('0', 'Organisation'),
    ('1', 'Own business'),
    ('2', 'User')
]
WORK_REG = [
    (0, '---'),
    (1, 'Mon-Fri'),
    (2, 'Mon-Sun'),
    (3, 'Mon-Sat'),
    (4, 'Sun-Sat'),
]
MEETING_TYPE = [
    (0, '---'),
    (1, '15m'),
    (2, '30m'),
    (3, '45m'),
    (4, '1h'),
    (5, '1d'),
]
CALENDAR_SCOPE = [
    (0, 'all'),
    (1, 'only friends'),
    (2, 'only me'),
]

class Profile(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="images/", default='../static/img/default-car.png')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=ROLE)
    work_regulations = models.IntegerField(choices=WORK_REG, default=0, null=True)
    available_from = models.TimeField(blank=True, null=True)
    available_to = models.TimeField(blank=True, null=True)
    meeting_type = models.IntegerField(choices=MEETING_TYPE, default=0, null=True)
    birthday = models.DateField()
    age = models.IntegerField()
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    adress = models.TextField(null=True, blank=True)
    calendar_scope = models.IntegerField(choices=CALENDAR_SCOPE)


    def save(self, *args, **kwargs):
        today = datetime.datetime.now(tz=get_current_timezone()).today()
        self.age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        super().save(*args, **kwargs)
