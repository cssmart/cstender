from django.db import models


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

    def __str__(self):
        return self.business_line
