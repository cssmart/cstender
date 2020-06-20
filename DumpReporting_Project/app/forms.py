from django import forms
from .models import DUMPReport, MRNReport, MRNReportGSTNew, ContributionReport,CustomerLedgerPassbook
from .popups import OrganisationIdPopupView, CustomerPopupView, CustomerSitePopupView
from django_popup_view_field.fields import PopupViewField, PopupViewModelField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import formset_factory
from django.http import HttpResponse
from django.db.models import CharField


class DumpForm(forms.ModelForm):
    class Meta:
        model = DUMPReport
        fields = ['table_type', 'business_line', 'business_unit', 'shipping_org','from_date', 'to_date',  'unit',
                  'sales_account']


class CustomerLdgerPassbookForm1(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       super(CustomerLdgerPassbookForm1, self).__init__(*args, **kwargs)
       self.fields['customer'].widget.attrs['readonly'] = True
    organisation = PopupViewField(view_class=OrganisationIdPopupView, required=True)
    customer = PopupViewField(view_class=CustomerPopupView, required=True)

    class Meta:
        model = CustomerLedgerPassbook
        fields = ['organisation','customer']


class CustomerLdgerPassbookForm2(forms.ModelForm):
    customer_site = PopupViewField(view_class=CustomerSitePopupView, required=False)

    class Meta:
        model = CustomerLedgerPassbook
        fields = ['customer_site', 'customer_type', 'start_date','end_date']
#



# class CustomerLedgerPassbookForm(forms.ModelForm):
#     organisation = PopupViewField(view_class=OrganisationIdPopupView, required=True)
#     print(organisation.callback_data,'kkkkkkkkkkkdddddddddddddddddddddddddddddddddddddddd')
#     customer = PopupViewField(view_class=CustomerPopupView, required=True)
#     # description = forms.CharField(widget=forms.TextInput,)
#     # customer_site = PopupViewField(view_class=CustomerSitePopupView, required=False)
#     # customer = PopupViewField(view_class=CustomerPopupView)
#     # customer_site = PopupViewField(view_class=CustomerSitePopupView)
#
#     # def save(self, commit=True):
#     #     instance = super(CustomerLedgerPassbookForm, self).save(commit=False)
#     #     print(instance,'xxxxxxxxxxxxxxxxxxxxeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
#     #     instance.organisation =forms.CharField()
#     #
#     #     if commit:
#     #         instance.save()
#     #     return instance
#
#     class Meta:
#         model = CustomerLedgerPassbook
#         fields = ['organisation','customer', 'customer_site', 'customer_type', 'start_date','end_date']
#     #
#
#     def form_valid(self, form):
#         organisation = form.cleaned_data.get("organisation")
#         print('organisation========',organisation)
#         return HttpResponse("Your color: {0}".format(organisation))
#
#
#     def __init__(self, *args, **kwargs):
#         print(kwargs,'ccccccccccccccccccccccccc222222222222222222222222222222222222222')
#         self.instance = kwargs.pop('instance', None)
#         print(self.instance,'xxxxxxxxxxxxxxxxxxxqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
#         super(CustomerLedgerPassbookForm, self).__init__(*args, **kwargs)
#         print(kwargs,args,'nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
#         self.data = self.data.copy()
#         print(self.data,'2222222222222444444444444444444444444446666666666666666666666666666666666')
#
#         self.helper = FormHelper()
#         print(self.helper,'helopppppppppppppppppppppppppppppppppppppppppppppppp')
#         # self.fields['organisation'] = CharField()
#         # print(self.fields['organisation'],'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
#         self.fields['customer_site'] = PopupViewField(
#             view_class=CustomerSitePopupView,
#             popup_dialog_title="Please select a reason for",
#             callback_data={
#                 'org_id': self.instance.customer,
#                 # 'c_id': self.fields['organisation'].initial
#             },
#             required=False,
#         )
#
#
#     # def __init__(self, *args, **kwargs):
#     #     # Get 'initial' argument if any
#     #     initial_arguments = kwargs.get('organisation', None)
#     #     print(initial_arguments,'llllllllllllllllllllllllllllllll')
#     #     updated_initial = {}
#     #     if initial_arguments:
#     #         print(initial_arguments,'lwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
#     #         # We have initial arguments, fetch 'user' placeholder variable if any
#     #         user = initial_arguments.get('user', None)
#     #         # Now update the form's initial values if user
#     #         if user:
#     #             updated_initial['name'] = getattr(user, 'first_name', None)
#     #             updated_initial['email'] = getattr(user, 'email', None)
#     #     # You can also initialize form fields with hardcoded values
#     #     # or perform complex DB logic here to then perform initialization
#     #     updated_initial['customer'] = 'Please provide a comment'
#     #     print( updated_initial['customer'],'lopopppppppppppppppppppppppppppppppppppppppp')
#     #     # Finally update the kwargs initial reference
#     #     kwargs.update(initial=updated_initial)
#     #     super(CustomerLedgerPassbookForm, self).__init__(*args, **kwargs)
#     # def __init__(self, args, **kwargs):
#     #     self.request = kwargs.pop('request', None)
#     #     print(self.request,'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
#     #     self.slug = kwargs.pop('slug', None)
#     #     print(self.slug,'kkkkkkkkkkwwwwwwwwwwwwwwwwwwwwwww')
#     #     super(CustomerLedgerPassbookForm, self).__init__(*args, **kwargs)
#     # def get_form(self, request, **kwargs):
#     #     form = super(CustomerLedgerPassbookForm, self).get_form(request, **kwargs)
#     #     print(form,'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
#     #     # form.organisation = request.user
#     #     return form
#
#     # def __init__(self, *args, **kwargs):
#     #     super(CustomerLedgerPassbookForm, self).__init__(*args, **kwargs)
#     #     print(super(CustomerLedgerPassbookForm, self).__init__(*args, **kwargs),'ooooooooooooooooooooo')
#     #     result_obj = self.instance
#     #     print(result_obj,kwargs, args,'llllllsoossjsjs')
#     #     self.helper = FormHelper()
#     #     self.helper.form_method = 'post'
#     #     self.helper.add_input(Submit('submit', 'Submit'))
#
#     # def __init__(self, *args, **kwargs):
#     #     print(kwargs,args,'dddddddddddd3333333333333333333333333333333333333')
#     #     super(CustomerLedgerPassbookForm, self).__init__(*args, **kwargs)
#     #     self.helper = FormHelper()
#     #     print(self.helper,'help===============================')
#     #     self.fields['organisation'] = forms.CharField()
#     #     print(self.fields['organisation'],'lllllllllllllllllllllooooooooooooooooooooooo')
#     #     self.fields['customer'] = forms.CharField()
#     #     initial = kwargs.get('initial', {})
#     #     print(initial,'ddddddddddddddddddddddddddddddddddd')
#     #     if initial:
#     #         id_value = initial['organisation']
#     #         print(id_value,'cccccccccccccccccc')
#     #     else:
#     #         id_value = 'None'
#     #         print('dddddddddddddddd')
#     #         self.fields['organisation'] = PopupViewField(
#     #             view_class=OrganisationIdPopupView,
#     #             popup_dialog_title="Please select a reason for the Attack Pattern",
#     #             # callback_data={'my_id': ID, 'other_param': 'xxx'},
#     #             required=True,
#     #         )
#     #         print(self.fields,'sssssssssssssssssssssssssssssssss')
#
#     # def __init__(self, *args, **kwargs):
#     #     super(CustomerLedgerPassbookForm, self).__init__(*args, **kwargs)
#     #     print(super(CustomerLedgerPassbookForm, self).__init__(*args, **kwargs),'kkkkkkkkkkkkkkk')
#     #     print(kwargs,args,'bbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
#     #     self.helper = FormHelper()
#     #     self.fields['organisation'] = forms.CharField()
#     #
#     #     initial = kwargs.get('initial', {})
#     #     print(initial,'cccccccccccccc')
#     #     if initial:
#     #         print('dddddddddddww')
#     #         id_value = initial['organisation']
#     #         print(id_value,'ddddddddddd')
#     #     else:
#     #         print('ccddcdcdddc')
#     #         id_value = 'None'
#     #
#     #     self.fields['organisation'] = PopupViewField(
#     #         view_class=OrganisationIdPopupView,
#     #         popup_dialog_title="Please select a reason for the Attack Pattern",
#     #         # callback_data={'my_id': ID, 'other_param': 'xxx'},
#     #         required=True,
#     #     )
#     #     print(self.fields['organisation'],'cccccccccccccwwwwwwwwwwwwwwwwwwwwwww')


# APReviewFormSet = formset_factory(CustomerLedgerPassbookForm, extra=0)

class ContributionReportForm(forms.ModelForm):
    class Meta:
        model = ContributionReport
        fields = ['table_type', 'ladger_id', 'unit', 'from_date', 'to_date']

class ContributionReportDownload(forms.ModelForm):
    class Meta:
        model = ContributionReport
        fields = ['report_type', 'ladger_id', 'unit', 'from_date', 'to_date']

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

class MRNReportGSTNewForm(forms.ModelForm):
    class Meta:
        model = MRNReportGSTNew
        fields = ['from_date', 'to_date']