from django import forms
from .models import DUMPReport, MRNReport


class DumpForm(forms.ModelForm):
    class Meta:
        model = DUMPReport
        fields = ['table_type', 'business_line', 'business_unit', 'shipping_org','from_date', 'to_date',  'unit',
                  'sales_account']

class MRNReportForm(forms.ModelForm):
    class Meta:
        model = MRNReport
        fields = ['table_type', 'inventory_org', 'item_category', 'from_date', 'to_date','vender', 'po_number',
                  'mrn_no','gate_entry_no','status']

class DumpDownloadForm(forms.ModelForm):
    class Meta:
        model = DUMPReport
        fields = ['report_type', 'business_line', 'business_unit', 'shipping_org','from_date', 'to_date',  'unit',
                  'sales_account']


class MRNReportDownloadForm(forms.ModelForm):
    class Meta:
        model = MRNReport
        fields = ['report_type', 'inventory_org', 'from_date', 'to_date','vender','gate_entry_no','status']