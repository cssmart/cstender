from django import forms
from material import Layout, Row, Span2
from . import models
from dal import autocomplete
# from django.http import JsonResponse, QueryDict
# from material.forms import AjaxModelSelect
import datetime


class TenderDetailForm(forms.ModelForm):
    layout = Layout(
        Row('tender_code','tender_creation_date', 'customer_name','project_name'),
    )

    class Meta:
        model = models.TenderDataDetails
        fields = ['tender_code', 'tender_creation_date', 'customer_name', 'project_name']

    def clean(self):
        super(TenderDetailForm, self).clean()
        tender_code = self.cleaned_data.get('tender_code')
        if len(tender_code) > 4:
            self._errors['tender_code'] = self.error_class([
                'Maximum 4 characters required'])
        return self.cleaned_data


class BodyDetailsForm(forms.ModelForm):
    layout = Layout(
        Row('panel_sheet','bus_bar','gland_comp'),
        Row(Span2('htc_bolt'), 'pvc_sleeves'),
        Row(Span2('base_frame'), 'shutter_mcc'),
        Row(Span2('epoxy_paint'),'shrouts'),
    )

    class Meta:
        model = models.BodyDetails
        fields = ['panel_sheet','bus_bar','gland_comp','htc_bolt', 'pvc_sleeves','base_frame', 'shutter_mcc','epoxy_paint','shrouts']
        # fields = '__all__'


class BoardSummaryForm(forms.ModelForm):
    layout = Layout(
        Row('board_code', 'board_desc'),
    )

    class Meta:
        model = models.BoardDetails
        fields = ['board_code', 'board_desc']


class BoardForm(forms.ModelForm):
    layout = Layout(
        Row('board_code'),
    )

    class Meta:
        model = models.BoardDetails
        fields = ['board_code']


class BoardlistForm(forms.ModelForm):
    layout = Layout(
        Row('board_code','board_desc'),
        Row('mcc_or_nonstan', 'mcc_description'),
        Row('control_bus_bar_qty','board_qty'),
        Row('indoor_or_outdoor','stand_or_non'),
        Row('hori_bus_bar_desc', 'phase'),
        Row('front_access_panel')
    )

    class Meta:
        model = models.BoardDetails
        fields = ['board_code', 'board_desc', 'mcc_description', 'hori_bus_bar_desc',
                  'control_bus_bar_qty', 'board_qty', 'stand_or_non', 'phase',
                  'mcc_or_nonstan', 'front_access_panel', 'indoor_or_outdoor']



class BoardDetailForm(forms.ModelForm):
    layout = Layout(
        Row('board_code','board_desc'),
        Row('mcc_or_nonstan', 'mcc_description'),
        Row('control_bus_bar_qty','board_qty'),
        Row('indoor_or_outdoor','stand_or_non'),
        Row('hori_bus_bar_desc', 'phase'),
        Row('front_access_panel')
    )

    class Meta:
        model = models.BoardDetails
        fields = ['board_code', 'board_desc', 'mcc_description', 'hori_bus_bar_desc',
                  'control_bus_bar_qty', 'board_qty', 'stand_or_non', 'phase',
                  'mcc_or_nonstan', 'front_access_panel', 'indoor_or_outdoor']

    # class Media:
    #     js = (
    #         'app.js',
    #     )


class ModuleDetailForm(forms.ModelForm):
    layout = Layout(
        Row('board_code', 'board_desc'),
        Row('module_code', 'module_desc'),
        Row('module_type', 'revision'),
        Row('bus_section', 'quantity'),
        Row('quantity2', 'quantity3'),
        Row('quantity4', 'quantity5'),
    )

    class Meta:
        model = models.ModuleDetails
        fields = ['board_code', 'board_desc', 'module_code',  'bus_section', 'module_type', 'revision', 'module_desc',
                  'quantity2', 'quantity3', 'quantity4', 'quantity5', 'quantity']

        # this function will be used for the validation
    def clean(self):

        # data from the form is fetched using super function
        super(ModuleDetailForm, self).clean()

        bus_section = self.cleaned_data.get('bus_section')
        quantity = self.cleaned_data.get('quantity')
        quantity2 = self.cleaned_data.get('quantity2')
        quantity3 = self.cleaned_data.get('quantity3')
        quantity4 = self.cleaned_data.get('quantity4')
        quantity5 = self.cleaned_data.get('quantity5')
        bus_list = ['1', '2', '3', '4', '5']
        if bus_section not in bus_list:
            self._errors['bus_section'] = self.error_class([
                'Please Enter Number between 1 to 5 '])
        if bus_section == '1' and quantity == 0:
            msg = forms.ValidationError("This field is required.")
            self.add_error('quantity', msg)

        if bus_section == '2' and (quantity == 0 or quantity2 == 0):
            msg = forms.ValidationError("This field is required.")
            self.add_error('quantity', msg)
            self.add_error('quantity2', msg)

        if bus_section == '3' and (quantity == 0 or quantity2 == 0 or quantity3 == 0):
            msg = forms.ValidationError("This field is required.")
            self.add_error('quantity', msg)
            self.add_error('quantity2', msg)
            self.add_error('quantity3', msg)

        if bus_section == '4' and (quantity == 0 or quantity2 == 0 or quantity3 == 0 or quantity4 == 0):
            msg = forms.ValidationError("This field is required.")
            self.add_error('quantity', msg)
            self.add_error('quantity2', msg)
            self.add_error('quantity3', msg)
            self.add_error('quantity4', msg)

        if bus_section == '5' and (quantity == 0 or quantity2 == 0 or quantity3 == 0 or quantity4 == 0 or quantity5 == 0):
            msg = forms.ValidationError("This field is required.")
            self.add_error('quantity', msg)
            self.add_error('quantity2', msg)
            self.add_error('quantity3', msg)
            self.add_error('quantity4', msg)
            self.add_error('quantity5', msg)

        module_type = self.cleaned_data.get('module_type')
        module_list = ['incoming', 'bus_coupler', 'outgoing']
        if module_type not in module_list:
            self._errors['module_type'] = self.error_class([
                'Please Enter the Correct module type'])
        return self.cleaned_data


class ComponentDetailForm(forms.ModelForm):
    layout = Layout(
        Row('module_code', 'module_desc'),
        Row('board_code', 'board_desc'),
        Row('component_id', 'component_desc'),
        Row('component_quantity'),
    )

    class Meta:
        model = models.ComponentDetails
        fields = ['module_code', 'module_desc', 'board_code', 'board_desc', 'component_id', 'component_desc',
                  'component_quantity']