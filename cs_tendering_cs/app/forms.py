from django import forms
from material import Layout, Row, Span2
from . import models


class TenderDetailForm(forms.ModelForm):
    layout = Layout(
        Row('tender_code', 'customer_name','project_name'),
    )
    class Meta:
        model = models.TenderDataDetails
        fields = ['tender_code', 'customer_name','project_name', ]


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


class BoardDetailForm(forms.ModelForm):
    layout = Layout(
        Row('board_code','board_desc'),
        Row('mcc_description', 'hori_bus_bar_desc'),
        Row('control_bus_bar_qty','board_qty'),
        Row('indoor_or_outdoor','stand_or_non'),
        Row('mcc_or_nonstan', 'phase'),
        Row('no_of_bus_section', 'front_access_panel')
    )

    class Meta:
        model = models.BoardDetails
        fields = ['board_code', 'board_desc', 'mcc_description', 'hori_bus_bar_desc',
                  'control_bus_bar_qty', 'board_qty', 'stand_or_non', 'phase',
                  'mcc_or_nonstan', 'front_access_panel', 'indoor_or_outdoor','no_of_bus_section']


class AddModuleForm(forms.ModelForm):
    layout = Layout(
        Row('board_detail'),
        Row('module_type', 'module_id'),
        Row('description')
    )

    class Meta:
        model = models.ModuleDetails
        fields = ['board_detail', 'module_type', 'module_id', 'description']


class ModuleDetailForm(forms.ModelForm):
    layout = Layout(
        Row('board_detail'),
        Row('type', 'bus_section'),
        Row('module_code', 'revision'),
        Row('description', 'quantity'),
        Row('quantity2', 'quantity3'),
        Row('quantity4', 'quantity5'),
    )

    class Meta:
        model = models.ModuleDetails
        fields = ['bus_section', 'type', 'module_code', 'revision', 'quantity',
                  'board_detail', 'description', 'quantity2', 'quantity3', 'quantity4', 'quantity5']