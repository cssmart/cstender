from django.db import models
from django.utils.translation import ugettext_lazy as _


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
    email_id = models.EmailField(default = None)
    contact_no = models.CharField(max_length=10, blank=True)
    department = models.CharField(max_length=100, blank=True)

    creation_date = models.CharField(max_length=120, blank=True)
    last_update_date = models.CharField(max_length=100, blank=True)
    created_by = models.CharField(max_length=200, blank=True)
    last_updated_by = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True,blank=True)
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
    project_name =models.CharField(max_length=100, blank=True)
    project_description =models.CharField(max_length=100, blank=True)
    application_id =models.ForeignKey(APPLICATION, on_delete=models.CASCADE, related_name="pro_application_id",blank=True, null=True)
    project_type =models.CharField(choices=p_type,max_length=15, blank=True)
    start_date = models.CharField(max_length=100, blank=True)
    end_date = models.CharField(max_length=100, blank=True)
    expected_end_date = models.CharField(max_length=100, blank=True)
    status = models.CharField(choices=[('New','New'),('WIP','WIP'),('On-Hold','On-Hold'),('Closed','Closed')],max_length=100, blank=True)
    task_creation = models.CharField(choices=[('self','Self'),('pm','PM')],max_length=100, blank=True)
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
    resource_role = models.CharField(choices=[('owner','Owner'),('manager','Manager'),('Co-ordinator','Co-ordinator'),('team','Team')],max_length=100, blank=True)
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
    status = models.CharField(choices=[('new','New'),('in_progress','In Progress'),('close','Close')], max_length=50, blank=True)
    creation_date = models.CharField(max_length=100, blank=True)
    last_update_date = models.CharField(max_length=100, blank=True)
    created_by = models.CharField(max_length=100, blank=True)
    last_updated_by = models.CharField(max_length=100, blank=True)
    segment_1 = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True, blank=True)

    segment_2 = models.CharField(max_length=100, blank=True)
    segment_3 = models.CharField(max_length=100, blank=True)
    segment_4 = models.CharField(max_length=100, blank=True)
    segment_5 = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.task_name


class DOCUMENT(models.Model):
    document_id = models.CharField(max_length=100, blank=True)
    document_name = models.CharField(max_length=100, blank=True)
    document_location = models.FileField(upload_to='Document_Upload_Folder/', blank=True,null=True)
    project_id = models.CharField(max_length=100, blank=True)
    task_id = models.CharField(max_length=100, blank=True)

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