from django import forms
from .models import DUMPReport


class DumpForm(forms.ModelForm):
    class Meta:
        model = DUMPReport
        fields = ['table_type', 'business_line', 'business_unit', 'shipping_org','from_date', 'to_date',  'unit',
                  'sales_account']


class DumpDownloadForm(forms.ModelForm):
    class Meta:
        model = DUMPReport
        fields = ['report_type', 'business_line', 'business_unit', 'shipping_org','from_date', 'to_date',  'unit',
                  'sales_account']