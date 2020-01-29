from django.db import models
# Create your models here.
from datetime import datetime
from django.conf import settings

class ERPReport(models.Model):
    business_line = models.CharField(max_length=100)
    business_unit = models.CharField(max_length=100)
    shipping_org = models.CharField(max_length=100)
    from_date =models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    unit = models.CharField(max_length=100, default="")
    sales_account = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.business_line

    @property
    def lifespan(self):
        print(self.from_date.strftime('%m/%d/%Y'),'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
        return '%s - present' % self.from_date.strftime('%m/%d/%Y')