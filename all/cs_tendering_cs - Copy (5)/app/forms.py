from django import forms
from material import Layout, Row, Span2
from . import models
from dal import autocomplete
# from django.http import JsonResponse, QueryDict
# from material.forms import AjaxModelSelect


class TenderDetailForm(forms.ModelForm):
    layout = Layout(
        Row('tender_code', 'customer_name','project_name'),
    )

    class Meta:
        model = models.TenderDataDetails
        fields = ['tender_code', 'customer_name','project_name']


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
        # widgets = {
        #             'board_code': autocomplete.ModelSelect2(url='app')
        #         }
        # widgets = {
        #     'city': AjaxModelSelect(lookups=['name__icontains'])
        # }
        # print(widgets,'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
        # print(widgets.values,'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')

    class Media:
        js = (
            'app.js',
        )


class AddModuleForm(forms.ModelForm):
    layout = Layout(
        Row('board_code'),
        Row('module_type', 'module_id'),
        Row('description')
    )

    class Meta:
        model = models.ModuleDetails
        fields = ['board_code', 'module_type', 'module_id', 'description']


class ModuleDetailForm(forms.ModelForm):
    layout = Layout(
        Row('board_code', ),
        Row('type', 'bus_section', 'tender_id'),
        Row('module_code', 'revision'),
        Row('description', 'quantity'),
        Row('quantity2', 'quantity3'),
        Row('quantity4', 'quantity5'),
    )

    class Meta:
        model = models.ModuleDetails
        fields = ['board_code', 'module_code',  'bus_section', 'tender_id', 'type', 'revision', 'description', 'quantity',
                  'quantity2', 'quantity3', 'quantity4', 'quantity5']


class ComponentDetailForm(forms.ModelForm):
    layout = Layout(
        Row('board_detail'),
        Row('component_id', 'description'),
        Row('quantity'),
    )

    class Meta:
        model = models.ComponentDetails
        fields = ['board_detail', 'component_id', 'description', 'quantity']