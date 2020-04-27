from django import forms
from .models import VisitorManagementForm, MobileRegistered, FrequentVisitors
from django_popup_view_field.fields import PopupViewField, PopupViewModelField
from .popups import MeetPersonPopupView, HostNAmePopupView


class VistiorsFormFrequent(forms.ModelForm):
    host_name = PopupViewField(view_class=HostNAmePopupView)
    class Meta:
        model = FrequentVisitors
        fields = ['visitor_name', 'mobile_number', 'company','host_department','host_name',
                  'visitor_valid_upto','pic', 'reason']


class VisitorManagementFormCreate(forms.ModelForm):
    person_to_meet = PopupViewField(view_class=MeetPersonPopupView)

    class Meta:
        model = VisitorManagementForm
        fields = ['name', 'contact_number', 'company', 'person_to_meet','reason','pic']


class VisitorManagementExcelRepot(forms.ModelForm):
    class Meta:
        model = VisitorManagementForm
        fields = ['name', 'contact_number', 'person_to_meet','v_date_time']


class VisitorImage(forms.ModelForm):
    class Meta:
        model = VisitorManagementForm
        fields = ['pic']


class MobileRegisteredForm(forms.ModelForm):
    class Meta:
        model = MobileRegistered
        fields = ['mobile_number']

