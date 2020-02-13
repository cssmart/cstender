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