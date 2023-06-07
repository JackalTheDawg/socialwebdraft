from django.db import models
from django.db import models
from django.db import models
import calendar
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class User_profile(models.Model, models.Manager):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DATE_CHOICES = [(str(i), str(i)) for i in range(1, 32)]
    MONTH_CHOICES = [(str(i), calendar.month_name[i]) for i in range(1, 13)]
    YEAR_CHOICES = reversed([(str(i), str(i)) for i in range(1950, 2006)])
    SEX = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    first_name = models.CharField(max_length=18, null=True)
    second_name = models.CharField(max_length=18, null=True)
    birthday = models.CharField(max_length=2, null=True, choices=DATE_CHOICES)
    birthday_month = models.CharField(max_length=9, null=True, choices=MONTH_CHOICES)
    birthday_year = models.CharField(max_length=4, null=True, choices=YEAR_CHOICES)
    profile_picture = models.ImageField(upload_to='media', null=True)
    sex = models.CharField(max_length=18, choices=SEX)


class Users_blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.CharField(max_length=130, blank=True, null=True)
    content = models.FileField(upload_to='users blog', null=True, blank=True)
    date = models.DateTimeField(null=True)
    page = models.IntegerField(null=True)