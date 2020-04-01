from django.db import models
from datetime import datetime

class VisitorManagementForm(models.Model):
    name = models.CharField(max_length=200, blank=True)
    contact_number = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=100, blank=True)
    person_to_meet = models.CharField(max_length=400, blank=True)
    v_date_time = models.CharField(max_length=100, blank=True)
    is_approved = models.BooleanField(blank=True, null=True)
    reason = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name




