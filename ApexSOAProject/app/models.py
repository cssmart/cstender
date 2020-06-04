from django.db import models


# Create your models here.
class ApexTable(models.Model):
    trx_label = models.IntegerField(blank=True)
    forwarded_to = models.IntegerField(blank=True)
    forwarded_by = models.IntegerField(blank=True)
    item_template = models.CharField(max_length=200, blank=True)
    apex_id =models.IntegerField(blank=True)
    apex_status = models.BooleanField(blank=True, null=True)
    mail_status = models.CharField(max_length=50, blank=True)
    sys_date = models.CharField(max_length=50, blank=True)
    sys_time = models.CharField(max_length=50, blank=True)
    item_code = models.CharField(max_length=400,blank=True)
    email = models.CharField(max_length=300, blank=True)
    initiator_email =models.CharField(max_length=300, blank=True)


