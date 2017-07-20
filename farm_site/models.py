from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group
from django.utils.translation import ugettext_lazy as _

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
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    street_address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    phone = models.CharField(max_length=12, default='206-555-5555')
    email = models.EmailField(_('email address'), unique=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def short_name(self):
        return "%s %s" % (self.first_name, self.last_name)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('member_id', 1)


        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    created_date = models.DateTimeField(
            default=timezone.now)
    member = models.ForeignKey(Member)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def is_staff(self):
        return True

    def get_short_name(self):
        return self.email

    def get_long_name(self):
        return self.email

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
    season = models.ForeignKey(Season)
    # default=Season.objects.get(current_season=True
    paid = models.BooleanField(default=False)
    box = models.CharField(max_length=7, choices=BOX_CHOICES, default='regular')
    eggs = models.CharField(max_length=10, choices=EGG_CHOICES, default='none')
    payment = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='check')

    def __str__(self):
        return "Name: %s, Season: %s, Location: %s" % (self.member, self.season, self.location)
