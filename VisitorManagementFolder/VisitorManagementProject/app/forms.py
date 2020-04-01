from django import forms
from .models import VisitorManagementForm
from django_popup_view_field.fields import PopupViewField, PopupViewModelField
from .popups import MeetPersonPopupView


class VisitorManagementFormCreate(forms.ModelForm):
    person_to_meet = PopupViewField(view_class=MeetPersonPopupView)
    class Meta:
        model = VisitorManagementForm
        fields = ['name', 'contact_number', 'company', 'person_to_meet','reason']
