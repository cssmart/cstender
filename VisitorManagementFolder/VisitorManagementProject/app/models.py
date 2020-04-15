from django.db import models
from datetime import datetime


class VisitorManagementForm(models.Model):
    name = models.CharField(max_length=200, blank=True)
    contact_number = models.CharField(max_length=10, blank=True)
    company = models.CharField(max_length=100, blank=True)
    person_to_meet = models.CharField(max_length=400, blank=True)
    v_date_time = models.CharField(max_length=100, blank=True)
    is_approved = models.BooleanField(blank=True, null=True)
    reason = models.CharField(max_length=255, blank=True)
    pic = models.ImageField(upload_to = 'images/', default = 'images/a.jpg')
    Approved_by = models.CharField(max_length=100, blank=True)
    Approve_CHOICES = [
        ('approve', 'Approve')
    ]
    approve_by_security = models.CharField(choices=Approve_CHOICES, max_length=9, blank=True)


    def __str__(self):
        return self.name


class FrequentVisitors(models.Model):
    visitor_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=10, unique=True)

    company = models.CharField(max_length=200)
    host_department = models.CharField(max_length=100)
    host_name = models.CharField(max_length=100)
    visitor_valid_upto = models.CharField(max_length=100)
    visitor_registration_date = models.CharField(max_length=100, blank=True)
    pic = models.ImageField(upload_to='images/', default='images/a.jpg')
    is_approved = models.BooleanField(blank=True, null=True)
    reason = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.mobile_number


class MobileRegistered(models.Model):
    mobile_number = models.CharField(max_length=10)
    f_visitor_in_time = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.mobile_number
