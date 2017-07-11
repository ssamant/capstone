from django.db import models
from django.utils import timezone

class Season(models.Model):
    year = models.CharField(max_length=4)
    current_season = models.BooleanField()

    def __str__(self): return self.year

class Location(models.Model):
    name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    current = models.BooleanField()

    def __str__(self):
        return self.name

    def current_signups(self):
        return self.signup_set.filter(season__current_season=True)


class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    street_address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    phone = models.CharField(max_length=12, default='206-555-5555')
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

class Signup(models.Model):
    BOX_CHOICES = (
        ('regular', 'Regular'),
        ('large', 'Large')
    )

    EGG_CHOICES = (
        ('none', 'None'),
        ('half-dozen', 'Half Dozen'),
        ('dozen', 'Dozen')
    )

    PAYMENT_CHOICES = (
        ('check', 'Mail check'),
        ('online', 'Online Bill Pay')
    )

    member = models.ForeignKey(Member)
    location = models.ForeignKey(Location)
    season = models.ForeignKey(Season, default=Season.objects.get(current_season=True).id)
    paid = models.BooleanField(default=False)
    box = models.CharField(max_length=7, choices=BOX_CHOICES, default='regular')
    eggs = models.CharField(max_length=10, choices=EGG_CHOICES, default='none')
    payment = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='check')

    def __str__(self):
        return "Name: %s, Year: %s" % (self.member, self.season)
