from django import forms
from .models import ERPReport


class ERPForm(forms.ModelForm):

    class Meta:
        model = ERPReport
        fields = ['business_line', 'business_unit', 'shipping_org','from_date', 'to_date',  'unit', 'sales_account']
