from django import forms
from django.forms import ClearableFileInput
from django.core.exceptions import ValidationError

from .models import UserTable,PROJECT,PROJECT_RESOURCES,PEOPLE,TASK,TEAM,DOCUMENT,APPLICATION,\
    NOTIFICATIONS
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['username'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['password1'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['password2'].widget.attrs['style'] = 'width:100%; height:40px;'


class DateInput(forms.DateInput):
    input_type = 'date'


class DOCUMENT_FORM(forms.ModelForm):
    class Meta:
        model = DOCUMENT
        fields = ['document_name','document_location','document_type']

    def __init__(self, *args, **kwargs):
        super(DOCUMENT_FORM, self).__init__(*args, **kwargs)
        self.fields['document_location'].required = True
        self.fields['document_type'].required = True
        self.fields['document_location'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['document_name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['document_type'].widget.attrs['style'] = 'width:100%; height:40px;'

from django.utils.translation import gettext_lazy as _

class TASK_FORM1(forms.ModelForm):
    class Meta:
        model = TASK
        fields = ['task_name','description', 'task_by','assigned_by','assigned_to','reassignable',
                  'status','start_date','end_date','expected_end_date','task_type','required_dba_processing']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
            'expected_end_date': DateInput()
        }
    def __init__(self, *args, **kwargs):
        super(TASK_FORM1, self).__init__(*args, **kwargs)
        self.fields['task_name'].required = True
        self.fields['description'].required = True
        # self.fields['parent_task'].required = False
        self.fields['assigned_by'].required = True
        self.fields['assigned_to'].required = True
        self.fields['task_by'].required = True
        self.fields['task_type'].required = True
        self.fields['end_date'].required = False
        self.fields['task_type'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['required_dba_processing'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['reassignable'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['start_date'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['end_date'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['task_name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['description'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['task_by'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['assigned_by'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['assigned_to'].widget.attrs['style'] = 'width:100%; height:40px;'
        # self.fields['parent_task'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['status'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['expected_end_date'].widget.attrs['style'] = 'width:100%; height:40px;'

class TASK_FORM(forms.ModelForm):
    class Meta:
        model = TASK
        fields = ['task_name','description','project_id', 'task_by','assigned_by','assigned_to','reassignable',
                  'status','parent_task','start_date','end_date','expected_end_date','task_type']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
            'expected_end_date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(TASK_FORM, self).__init__(*args, **kwargs)
        self.fields['task_name'].required = True
        self.fields['description'].required = True
        self.fields['parent_task'].required = False
        self.fields['assigned_by'].required = True
        self.fields['assigned_to'].required = True
        self.fields['task_by'].required = True
        self.fields['task_type'].required = True
        self.fields['task_type'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['reassignable'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['start_date'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['end_date'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['task_name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['description'].widget.attrs['style'] = 'width:100%; height:40px;'
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


class EDIT_PROJET_FORM(forms.ModelForm):
    class Meta:
        model = PROJECT
        fields = ['project_description','project_type',
                  'expected_end_date','status','task_creation','self_task_reasignment',
                  'project_business_owner', 'project_objective'
                  ]
        widgets = {
            'expected_end_date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(EDIT_PROJET_FORM, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['self_task_reasignment'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['expected_end_date'].widget.attrs['style'] = 'width:100%; height:50px;'
        self.fields['project_description'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['project_type'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['task_creation'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['project_objective'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['project_business_owner'].widget.attrs['style'] = 'width:100%; height:40px;'


class PROJET_FORM(forms.ModelForm):
    class Meta:
        model = PROJECT
        fields = ['project_name', 'project_description','application_id','project_type','start_date',
                  'expected_end_date','status','task_creation','self_task_reasignment',
                  'project_business_owner','project_objective']
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
        self.fields['project_objective'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['project_business_owner'].widget.attrs['style'] = 'width:100%; height:40px;'


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
        fields = ['project_id','team_resource_id','resource_pool','team_resource_role']

    def __init__(self, *args, **kwargs):
        super(PROJECT_RESOURCES_TEAM_FORM, self).__init__(*args, **kwargs)
        self.fields['team_resource_id'].required = True
        self.fields['team_resource_id'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['project_id'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['resource_pool'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['team_resource_role'].widget.attrs['style'] = 'width:100%; height:40px;'


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
        fields = ['p_first_name', 'p_last_name', 'email_id',
                  'contact_no', 'department','can_create_project','can_create_application','can_create_people']

    def __init__(self, *args, **kwargs):
        super(PEOPLE_FORM, self).__init__(*args, **kwargs)
        self.fields['p_first_name'].required = True
        self.fields['p_last_name'].required = True
        self.fields['email_id'].required = True
        self.fields['contact_no'].required = True
        self.fields['department'].required = True
        self.fields['department'].required = True
        self.fields['email_id'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['can_create_application'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['can_create_project'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['can_create_people'].widget.attrs['style'] = 'width:100%; height:40px;'
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

    def __init__(self, *args, **kwargs):
        super(TEAM_FORM1, self).__init__(*args, **kwargs)
        self.fields['team_name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['team_description'].widget.attrs['style'] = 'width:100%; height:40px;'


class TEAM_FORM2(forms.ModelForm):
    class Meta:
        model = TEAM
        fields = ['team_member']
    def __init__(self, *args, **kwargs):
        super(TEAM_FORM2, self).__init__(*args, **kwargs)
        self.fields['team_member'].widget.attrs['style'] = 'width:100%; height:40px;'
