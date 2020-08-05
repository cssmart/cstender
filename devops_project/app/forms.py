from django import forms
from django.forms import ClearableFileInput

from .models import UserTable,PROJECT,PROJECT_RESOURCES,PEOPLE,TASK,TEAM,DOCUMENT,APPLICATION,\
    NOTIFICATIONS


class DateInput(forms.DateInput):
    input_type = 'date'

class DOCUMENT_FORM(forms.ModelForm):
    class Meta:
        model = DOCUMENT
        fields = ['document_name','document_location']


class TASK_FORM(forms.ModelForm):
    class Meta:
        model = TASK
        fields = ['task_name','description','project_id', 'task_by','assigned_by','assigned_to','reassignable',
                  'status','parent_task','start_date','end_date','expected_end_date']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
            'expected_end_date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(TASK_FORM, self).__init__(*args, **kwargs)
        self.fields['parent_task'].required = False
        self.fields['project_id'].required = True
        self.fields['reassignable'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['start_date'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['end_date'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['task_name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['description'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['project_id'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['task_by'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['assigned_by'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['assigned_to'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['parent_task'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['status'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['expected_end_date'].widget.attrs['style'] = 'width:100%; height:40px;'


class UserFomr(forms.ModelForm):
    class Meta:
        model = UserTable
        fields = ['username', 'first_name','last_name','email_id','contact_no','segment1','segment2',
                  'segment3']


class PROJET_FORM(forms.ModelForm):
    # application_id = forms.CharField(required=True)

    class Meta:
        model = PROJECT
        fields = ['project_name', 'project_description','application_id','project_type','start_date',
                  'expected_end_date','status','task_creation','self_task_reasignment']
        widgets = {
            'start_date': DateInput(),
            'expected_end_date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(PROJET_FORM, self).__init__(*args, **kwargs)
        self.fields['application_id'].required = False
        self.fields['status'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['self_task_reasignment'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['start_date'].widget.attrs['style'] = 'width:100%; height:50px;'
        self.fields['expected_end_date'].widget.attrs['style'] = 'width:100%; height:50px;'
        self.fields['project_name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['project_description'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['application_id'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['project_type'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['task_creation'].widget.attrs['style'] = 'width:100%; height:40px;'


class PROJECT_RESOURCES_FORM(forms.ModelForm):
    class Meta:
        model = PROJECT_RESOURCES
        fields = ['project_id', 'individual_resource_id','resource_pool','resource_role']

    def __init__(self, *args, **kwargs):
        super(PROJECT_RESOURCES_FORM, self).__init__(*args, **kwargs)
        self.fields['individual_resource_id'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['project_id'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['resource_pool'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['resource_role'].widget.attrs['style'] = 'width:100%; height:40px;'


class PROJECT_RESOURCES_TEAM_FORM(forms.ModelForm):
    class Meta:
        model = PROJECT_RESOURCES
        fields = ['project_id','team_resource_id','resource_pool','resource_role']

    def __init__(self, *args, **kwargs):
        super(PROJECT_RESOURCES_TEAM_FORM, self).__init__(*args, **kwargs)
        self.fields['team_resource_id'].required = True
        self.fields['team_resource_id'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['project_id'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['resource_pool'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['resource_role'].widget.attrs['style'] = 'width:100%; height:40px;'


class APPLICATION_FORM(forms.ModelForm):
    class Meta:
        model = APPLICATION
        fields = ['application_name','application_description']

    def __init__(self, *args, **kwargs):
        super(APPLICATION_FORM, self).__init__(*args, **kwargs)
        self.fields['application_name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['application_description'].widget.attrs['style'] = 'width:100%; height:40px;'


class PEOPLE_FORM(forms.ModelForm):

    class Meta:
        model = PEOPLE
        fields = [ 'p_first_name', 'p_last_name', 'email_id',
                  'contact_no', 'department']

    def __init__(self, *args, **kwargs):
        super(PEOPLE_FORM, self).__init__(*args, **kwargs)
        self.fields['email_id'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['p_first_name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['p_last_name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['contact_no'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['department'].widget.attrs['style'] = 'width:100%; height:40px;'


class TEAM_FORM1(forms.ModelForm):
    team_name = forms.CharField(required=True)
    team_description = forms.CharField(required=True)
    class Meta:
        model = TEAM
        fields = ['team_name', 'team_description']


class TEAM_FORM2(forms.ModelForm):
    class Meta:
        model = TEAM
        fields = ['team_member']