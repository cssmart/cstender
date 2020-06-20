from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model

User = get_user_model()
print(User.first_name,'dddddddddddddddddddddd')


class UserForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.TextField()

    # def __str__(self):
    #     return self.user_id

    def save(self, *args, **kwargs):
        userObj = self.user
        userObj.is_staff = True
        userObj.save()
        super(UserForm, self).save(*args, **kwargs)


class DUMPReport(models.Model):
    business_line = models.CharField(max_length=100, blank=True)
    business_unit = models.CharField(max_length=100, blank=True)
    shipping_org = models.CharField(max_length=100, blank=True)
    from_date = models.CharField(max_length=11)
    to_date = models.CharField(max_length=11)
    unit = models.CharField(max_length=100, default="", blank=True)
    sales_account = models.CharField(max_length=200, default="", blank=True)
    table_type = models.CharField(choices=[('create&insert', 'Create & Insert'), ('create_table', 'Create'),
                                           ('insert', 'Insert'), ('replace', 'Replace')], max_length=20)
    report_type = models.CharField(choices=[('pdf', 'PDF'), ('excel', 'Excel')], max_length=10)

    def __str__(self):
        return self.business_line


class MRNReport(models.Model):
    table_type = models.CharField(choices=[('create&insert', 'Create & Insert'), ('create_table', 'Create'),
                                           ('insert', 'Insert'), ('replace', 'Replace')], max_length=20)
    inventory_org = models.CharField(max_length=100, blank=True)
    item_category = models.CharField(max_length=100, blank=True)
    from_date = models.CharField(max_length=50)
    to_date = models.CharField(max_length=50)
    vender = models.CharField(max_length=100,blank=True)
    po_number = models.CharField(max_length=200, blank=True)
    item = models.CharField(max_length=100, blank=True)
    mrn_no = models.CharField(max_length=100, blank=True)
    gate_entry_no = models.CharField(max_length=100, blank=True)
    invoice_no = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=100, blank=True)
    report_type = models.CharField(choices=[('pdf', 'PDF'), ('excel', 'Excel')], max_length=10)

    def __str__(self):
        return self.po_number


class MRNReportGSTNew(models.Model):

    from_date = models.CharField(max_length=50, blank=True,)
    to_date = models.CharField(max_length=50, blank=True)


class ContributionReport(models.Model):
    table_type = models.CharField(choices=[('create&insert', 'Create & Insert'), ('create_table', 'Create'),
                                           ('insert', 'Insert'), ('replace', 'Replace')], max_length=20)
    unit = models.CharField(max_length=100, blank=True)
    from_date = models.CharField(max_length=100, blank=True)
    to_date = models.CharField(max_length=100, blank=True)
    ladger_id = models.CharField(max_length=100, blank=True)
    report_type = models.CharField(choices=[('pdf', 'PDF'), ('excel', 'Excel')], max_length=10)


class CustomerLedgerPassbook(models.Model):
    organisation = models.CharField(max_length=500, blank=True)
    customer =models.CharField(max_length=400, blank=True, null=True)
    customer_number = models.CharField(max_length=100, blank=True)
    customer_site = models.CharField(max_length=500, blank=True)
    customer_type = models.CharField(max_length=500, blank=True)
    start_date = models.CharField(max_length=50)
    end_date =models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        super(CustomerLedgerPassbook, self).save(*args, **kwargs)
