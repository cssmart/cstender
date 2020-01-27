from django.db import models
# Create your models here.
from datetime import datetime

class ERPReport(models.Model):
    business_line = models.CharField(max_length=100)
    business_unit = models.CharField(max_length=100)
    shipping_org = models.CharField(max_length=100)
    from_date =models.DateTimeField(default=datetime.now, blank=True)
    to_date = models.DateTimeField()
    unit = models.CharField(max_length=100, default="")
    sales_account = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.business_line