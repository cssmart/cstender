from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class UserForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    people_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return 'User id: '+str(self.user.username)+' , '+'People: '+self.people_id

    def save(self, *args, **kwargs):
        userObj = self.user
        userObj.is_staff = True
        userObj.save()
        super(UserForm, self).save(*args, **kwargs)


class APPLICATION(models.Model):
    application_id = models.CharField(max_length=100, blank=True)
    application_name = models.CharField(max_length=100, blank=True)
    application_description = models.CharField(max_length=100, blank=True)

    creation_date = models.CharField(max_length=100, blank=True)
    last_update_date = models.CharField(max_length=100, blank=True)
    created_by = models.CharField(max_length=100, blank=True)
    last_updated_by = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True, blank=True)
    segment_1 = models.CharField(max_length=100, blank=True)
    segment_2 = models.CharField(max_length=100, blank=True)
    segment_3 = models.CharField(max_length=100, blank=True)
    segment_4 = models.CharField(max_length=100, blank=True)
    segment_5 = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.application_name


class PEOPLE(models.Model):
    res_pool = [
        ('individual', 'Individual'),
        ('team', 'Team')
    ]
    p_first_name = models.CharField(max_length=100, blank=True)
    p_last_name = models.CharField(max_length=100, blank=True)
    email_id = models.EmailField(default=None)
    contact_no = models.CharField(max_length=10, blank=True)
    department = models.CharField(max_length=200, blank=True)

    creation_date = models.CharField(max_length=120, blank=True)
    last_update_date = models.CharField(max_length=100, blank=True)
    created_by = models.CharField(max_length=200, blank=True)
    last_updated_by = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True,blank=True)
    can_create_application = models.BooleanField(default=False,blank=True)
    can_create_project = models.BooleanField(default=False,blank=True)
    can_create_people = models.BooleanField(default=False,blank=True)
    segment_1 = models.CharField(max_length=100, blank=True)
    segment_2 = models.CharField(max_length=100, blank=True)
    segment_3 = models.CharField(max_length=100, blank=True)
    segment_4 = models.CharField(max_length=100, blank=True)
    segment_5 = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.p_first_name +' '+self.p_last_name + ' (' + self.email_id + ')'


class TEAM(models.Model):
    res_pool=[
        ('individual','Individual'),
        ('team','Team')
    ]
    team_id =models.CharField(max_length=100, blank=True)
    team_name =models.CharField(max_length=100, blank=True)
    team_description =models.CharField(max_length=200, blank=True)
    team_member =models.ForeignKey(PEOPLE, on_delete=models.CASCADE, related_name="team_member_id",blank=False, null=True)

    creation_date = models.CharField(max_length=100, blank=True)
    all_members = models.TextField(default='0')
    last_update_date = models.CharField(max_length=100, blank=True)
    created_by = models.CharField(max_length=100, blank=True)
    last_updated_by = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=True,blank=True)
    segment_1 = models.CharField(max_length=100, blank=True)
    segment_2 = models.CharField(max_length=100, blank=True)
    segment_3 = models.CharField(max_length=100, blank=True)
    segment_4 = models.CharField(max_length=100, blank=True)
    segment_5 = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.team_name


class PROJECT(models.Model):
    p_type=[
        ('development','Development'),
        ('support','Support')
    ]
    login_create_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
    project_name =models.CharField(max_length=100, blank=True)
    project_description =models.CharField(max_length=100, blank=True)
    application_id =models.ForeignKey(APPLICATION, on_delete=models.CASCADE, related_name="pro_application_id",blank=True, null=True)
    project_type =models.CharField(choices=p_type,max_length=15, blank=True)
    start_date = models.CharField(max_length=100, blank=True)
    end_date = models.CharField(max_length=100, blank=True)
    project_objective = models.TextField(blank=True,null=True)
    project_business_owner = models.TextField(blank=True,null=True)
    expected_end_date = models.CharField(max_length=50, blank=True)
    initial_exp_completion_dt = models.CharField(max_length=150, blank=True)
    status = models.CharField(choices=[('New','New'),('WIP','WIP'),('On-Hold','On-Hold'),('Closed','Closed')],max_length=100, blank=True)
    task_creation = models.CharField(choices=[('self','Self'),('owner','Owner')],max_length=100, blank=True)
    self_task_reasignment = models.BooleanField(default=False, blank=True)
    creation_date = models.CharField(max_length=100, blank=True)
    last_update_date = models.CharField(max_length=100, blank=True)
    created_by = models.CharField(max_length=100, blank=True)
    last_updated_by = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True, blank=True)
    segment_1 = models.CharField(max_length=100, blank=True)
    segment_2 = models.CharField(max_length=100, blank=True)
    segment_3 = models.CharField(max_length=100, blank=True)
    segment_4 = models.CharField(max_length=100, blank=True)
    segment_5 = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.project_name


class PROJECT_RESOURCES(models.Model):
    res_pool=[
        ('individual','Individual'),
        ('team','Team')
    ]
    line_id =models.CharField(max_length=100, blank=True)
    project_id =models.ForeignKey(PROJECT, on_delete=models.CASCADE, related_name="project_member",blank=True, null=True)
    individual_resource_id =models.ForeignKey(PEOPLE, on_delete=models.CASCADE, related_name="individual_member",blank=True, null=True)
    team_resource_id =models.ForeignKey(TEAM, on_delete=models.CASCADE, related_name="team_members",blank=True, null=True)
    resource_id =models.CharField(max_length=100, blank=True)
    resource_pool =models.CharField(choices=res_pool,max_length=15, blank=True)
    resource_role = models.CharField(choices=[('owner','Owner'),('manager','Manager'),('Co-ordinator','Co-ordinator'),('team','Team'),('dba','DBA')],max_length=100, blank=True)
    team_resource_role = models.CharField(choices=[('manager','Manager'),('Co-ordinator','Co-ordinator'),('team','Team')],max_length=100, blank=True)

    creation_date = models.CharField(max_length=100, blank=True)
    last_update_date = models.CharField(max_length=100, blank=True)
    created_by = models.CharField(max_length=100, blank=True)
    last_updated_by = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True, blank=True)
    segment_1 = models.CharField(max_length=100, blank=True)
    segment_2 = models.CharField(max_length=100, blank=True)
    segment_3 = models.CharField(max_length=100, blank=True)
    segment_4 = models.CharField(max_length=100, blank=True)
    segment_5 = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.resource_role


class TASK(models.Model):
    task_id = models.CharField(max_length=100, blank=True)
    # project_id = models.CharField(max_length=100, blank=True)
    task_name = models.CharField(max_length=300, blank=True)
    description = models.CharField(max_length=300, blank=True)
    task_by = models.ForeignKey(PEOPLE, on_delete=models.CASCADE, related_name="task_by",blank=True, null=True)
    project_id = models.ForeignKey(PROJECT, on_delete=models.CASCADE, related_name="project_by",blank=True, null=True)
    assigned_by = models.ForeignKey(PEOPLE, on_delete=models.CASCADE, related_name="assigned_by",blank=True, null=True)
    assigned_to = models.ForeignKey(PEOPLE, on_delete=models.CASCADE, related_name="assigned_to",blank=True, null=True)
    reassignable= models.BooleanField(default=False, blank=True)
    # parent_task = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    parent_task = models.ForeignKey('self',on_delete=models.CASCADE, blank=True, null=True)

    start_date = models.CharField(max_length=70, blank=True)
    end_date = models.CharField(max_length=100, blank=True)
    expected_end_date = models.CharField(max_length=100, blank=True)
    initial_expected_end_date = models.CharField(max_length=100, blank=True)
    status = models.CharField(choices=[('new','New'),('in_progress','In Progress'),('close','Close')], max_length=50, blank=True)
    task_type = models.CharField(choices=[('support','Support'),('change','Change')], max_length=50, blank=True)
    approval_flag = models.CharField(choices=[('Not Required','Not Required'),('on_going','On Going'),('complete','Complete')], max_length=50, blank=True)
    creation_date = models.CharField(max_length=100, blank=True)
    last_update_date = models.CharField(max_length=100, blank=True)
    created_by = models.CharField(max_length=100, blank=True)
    last_updated_by = models.CharField(max_length=100, blank=True)
    segment_1 = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True, blank=True)
    required_dba_processing = models.BooleanField(default=False, blank=True)
    task_complete = models.BooleanField(default=False, blank=True)
    segment_2 = models.CharField(max_length=100, blank=True)
    segment_3 = models.CharField(max_length=100, blank=True)
    segment_4 = models.CharField(max_length=100, blank=True)
    segment_5 = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.task_name


class TASK_APPROVALS(models.Model):
    task_id = models.ForeignKey(TASK, on_delete=models.CASCADE, related_name="task_idd",blank=True, null=True)
    approval_level = models.CharField(max_length=100, blank=True)
    executed = models.CharField(max_length=100, blank=True)
    note = models.CharField(max_length=100, blank=True, null=True)
    forwarded_note = models.TextField(blank=True, null=True)
    approval_status = models.CharField(max_length=100,  blank=True)
    forwarded_by = models.ForeignKey(PEOPLE, on_delete=models.CASCADE, related_name="forward_by",blank=True, null=True)
    forwarded_to = models.ForeignKey(PEOPLE, on_delete=models.CASCADE, related_name="forward_to",blank=True, null=True)

    def __str__(self):
        return 'Task Name: '+str(self.task_id)+' , '+'Approval Level: '+self.approval_level


class APPROVAL_HIERARCHY(models.Model):
    '''
    HIERARCHY_LINE_ID, PROJECT_ID,FORWARDED_BY,FORWARDED_TO,APPROVAL_LEVEL,TYPE (Parallel/Alternate)
    '''
    hierarchy_line_id = models.CharField(max_length=100, blank=True)
    approval_level = models.CharField(max_length=100, blank=True)
    type = models.CharField(choices=[('parallel','Parallel'),('alternate','Alternate')], max_length=50, blank=True)
    forwarded_by = models.ForeignKey(PEOPLE, on_delete=models.CASCADE, related_name="forwardd_by",blank=True, null=True)
    project_id = models.ForeignKey(PROJECT, on_delete=models.CASCADE, related_name="projects_id",blank=True, null=True)
    forwarded_to = models.ForeignKey(PEOPLE, on_delete=models.CASCADE, related_name="forwardd_to",blank=True, null=True)

    def __str__(self):
        return 'approval_level: '+ self.approval_level+' , '+'project_id: '+str(self.project_id)+','+'forwarded_to '+str(self.forwarded_to)

class DOCUMENT(models.Model):
    document_id = models.CharField(max_length=100, blank=True)
    document_name = models.CharField(max_length=100, blank=True)
    document_location = models.FileField(upload_to='Document_Upload_Folder/', blank=True,null=True)
    project_id = models.CharField(max_length=100, blank=True)
    task_id = models.CharField(max_length=100, blank=True)
    document_type = models.CharField(choices=[('Requirement Document',' Requirement Document'),('Technical Design','Technical Design'),('Functional Design','Functional Design'),(' Test Script',' Test Script')], max_length=100, blank=True)
    # Requirement Document, Technical Design, Functional Design, Test Script
    creation_date = models.CharField(max_length=100, blank=True)
    last_update_date = models.CharField(max_length=100, blank=True)
    created_by = models.CharField(max_length=100, blank=True)
    last_updated_by = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True, blank=True)
    segment_1 = models.CharField(max_length=100, blank=True)
    segment_2 = models.CharField(max_length=100, blank=True)
    segment_3 = models.CharField(max_length=100, blank=True)
    segment_4 = models.CharField(max_length=100, blank=True)
    segment_5 = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.document_location)


class UserTable(models.Model):
    username = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    email_id = models.CharField(max_length=200, blank=True)
    contact_no = models.CharField(max_length=10, blank=True)
    segment1 = models.CharField(max_length=200, blank=True)
    segment2 = models.CharField(max_length=200, blank=True)
    segment3 = models.CharField(max_length=200, blank=True)


class NOTIFICATIONS(models.Model):
    notification_id = models.CharField(max_length=100, blank=True)
    notification_type = models.CharField(max_length=100, blank=True)
    notification_description = models.CharField(max_length=100, blank=True)
    project_id = models.ForeignKey(PROJECT, on_delete=models.CASCADE, related_name="project_id",blank=True, null=True)
    task_id = models.ForeignKey(TASK, on_delete=models.CASCADE, related_name="task_select_id",blank=True, null=True)
    resource_id = models.ForeignKey(PROJECT_RESOURCES, on_delete=models.CASCADE, related_name="resource_type_id",blank=True, null=True)
    creation_date = models.CharField(max_length=100, blank=True)
    last_update_date = models.CharField(max_length=100, blank=True)
    created_by = models.CharField(max_length=100, blank=True)
    last_updated_by = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True, blank=True)
    segment_1 = models.CharField(max_length=100, blank=True)
    segment_2 = models.CharField(max_length=100, blank=True)
    segment_3 = models.CharField(max_length=100, blank=True)
    segment_4 = models.CharField(max_length=100, blank=True)
    segment_5 = models.CharField(max_length=200, blank=True)