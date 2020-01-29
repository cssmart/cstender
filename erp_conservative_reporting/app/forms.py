from django import forms
from .models import ERPReport


class ERPForm(forms.ModelForm):
    from_date = forms.DateField(
        widget=forms.widgets.DateInput(format="%m/%d/%Y"))
    print(from_date,'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')

    class Meta:
        model = ERPReport
        fields = ['business_line', 'business_unit', 'shipping_org','from_date', 'to_date',  'unit', 'sales_account']
