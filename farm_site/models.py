from django.db import models
from django.utils import timezone

class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    street_address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.last_name
