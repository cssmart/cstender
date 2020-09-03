from .models import PEOPLE, TEAM, PROJECT, PROJECT_RESOURCES, TASK, APPLICATION, NOTIFICATIONS, \
    DOCUMENT, UserForm, APPROVAL_HIERARCHY, TASK_APPROVALS
from .forms import PEOPLE_FORM, TEAM_FORM1, TEAM_FORM2, PROJET_FORM, PROJECT_RESOURCES_FORM, \
    PROJECT_RESOURCES_TEAM_FORM, TASK_FORM, APPLICATION_FORM, \
    DOCUMENT_FORM, TASK_FORM1, SignUpForm, EDIT_PROJET_FORM,TASK_APPROVALS_FORM,TASK_EDIT_FORM
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import redirect, render_to_response, get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from datetime import datetime
from django.db import connection
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import permission_required, login_required

from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from datetime import date
from datetime import date

User = get_user_model()


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")

def task_summary_edit(request,pk):
    search_approval_flag = TASK.objects.filter(id=pk).values('approval_flag')
    if search_approval_flag[0]['approval_flag'] == 'Approved' or search_approval_flag[0]['approval_flag'] =='on_going':
        message = 'You do not have sufficient privilages to edit this task '
        return render(request, 'error_page.html', {'message': message})
    # else:

    return HttpResponse('done')


def approval_notification_task_action_view(request, pk, t_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    form = TASK_APPROVALS_FORM(request.POST or None)
    if form.is_valid():
        form_1 = form.save(commit=False)
        forwarded_note = form.cleaned_data['forwarded_note']
        if forwarded_note:
            update_note = TASK_APPROVALS.objects.filter(id=pk).update(forwarded_note=forwarded_note)
        else:
            update_note = TASK_APPROVALS.objects.filter(id=pk).update(forwarded_note=None)
        return redirect(f'/notification_{pk}_{t_id}')
    # context = {
    #     "pk": pk,
    #     "form": form
    # }
    # return render(request, 'approval_notification_task_view.html', context)
    document = DOCUMENT.objects.filter(task_id=t_id)
    task = TASK.objects.filter(id=t_id)
    cursor = connection.cursor()
    task_details = f'''SELECT task_by_id, assigned_by_id,assigned_to_id
        FROM public.app_task where id='{t_id}';
    '''
    cursor.execute(task_details)
    task_details_ = cursor.fetchall()
    for i in task_details_:
        assign_to_ = i[2],
        assign_by_ = i[1],
        task_by_ = i[0]
        assign_to_id = str(assign_to_).replace("(", '').replace(",)", '')
        assign_by_id = str(assign_by_).replace("(", '').replace(",)", '')
        task_by_id = str(task_by_).replace("(", '').replace(",)", '')
        assign_to = PEOPLE.objects.filter(id=assign_to_id).values('p_first_name', 'p_last_name')
        assign_by = PEOPLE.objects.filter(id=assign_by_id).values('p_first_name', 'p_last_name')
        task_by = PEOPLE.objects.filter(id=task_by_id).values('p_first_name', 'p_last_name')
        context = {
            "task": task,
            "document": document,
            "assign_to": assign_to,
            "assign_by": assign_by,
            "task_by": task_by,
            "pk":pk,
            "form":form
        }
        return render(request, 'approval_notification_task_view.html', context)

def home_my_task_list_view(request):
    user_id = request.user.id
    p_id = UserForm.objects.filter(user_id=user_id).values('people_id')
    if p_id:
        ppl_id = p_id[0]['people_id']
        task_search = TASK.objects.all().filter(assigned_to_id=ppl_id)
        return render(request, 'home_my_task_view.html', {'task_search': task_search})
    else:
        message = 'You do not have sufficient privilages to show this details '
        return render(request, 'error_page.html', {'message': message})


def task_workshow_in_task_summary(request, pk):
    task_approval = TASK_APPROVALS.objects.filter(task_id_id=pk).values('id', 'approval_level',
                     'approval_status',
                    'forwarded_by_id', 'forwarded_to_id','forwarded_note','executed',
                    'task_id_id', 'note').order_by('approval_level')
    if task_approval:
        approval_id = []
        approval_level = []
        executed = []
        approval_status = []
        forwarded_by = []
        forwarded_to = []
        forwarded_note = []
        for i in task_approval:
            id_ = i['id']
            approval_id.append(id_)
            approval_level_ = i['approval_level']
            approval_level.append(approval_level_)
            executed_ = i['executed']
            executed.append(executed_)
            approval_status_ = i['approval_status']
            approval_status.append(approval_status_)
            forwarded_note_ = i['forwarded_note']
            forwarded_note.append(forwarded_note_)
            forwarded_by_ = i['forwarded_by_id']
            forwarded_name_by = PEOPLE.objects.filter(id=forwarded_by_).values('p_first_name', 'p_last_name')
            by_name = forwarded_name_by[0]['p_first_name'] + ' ' + forwarded_name_by[0]['p_last_name']
            forwarded_by.append(by_name)
            forwarded_to_ = i['forwarded_to_id']
            forwarded_name_to = PEOPLE.objects.filter(id=forwarded_to_).values('p_first_name', 'p_last_name')
            to_name = forwarded_name_to[0]['p_first_name'] + ' ' + forwarded_name_to[0]['p_last_name']

            forwarded_to.append(to_name)
        approval_data = zip(approval_id, approval_level, approval_status, forwarded_by, forwarded_to,forwarded_note)
        task = TASK.objects.filter(id=pk).values('task_name', 'project_id_id')
        task_name = task[0]['task_name']
        project_id = task[0]['project_id_id']
        approval_hierarchy = APPROVAL_HIERARCHY.objects.filter(project_id_id=project_id).values('id',
                                    'approval_level', 'type', 'forwarded_by_id', 'forwarded_to_id',
                                     'project_id').order_by('approval_level')
        approval_id = []
        approval_level = []
        type = []
        project_id_id = []
        forwarded_by = []
        forwarded_to = []
        for approval in approval_hierarchy:
            id_ = approval['id']
            approval_id.append(id_)
            approval_level_ = approval['approval_level']
            approval_level.append(approval_level_)
            type_ = approval['type']
            type.append(type_)
            project_id_id_ = approval['project_id']
            project_id_id.append(project_id_id_)
            forwarded_by_ = approval['forwarded_by_id']
            forwarded_name_by = PEOPLE.objects.filter(id=forwarded_by_).values('p_first_name', 'p_last_name')
            by_name = forwarded_name_by[0]['p_first_name'] + ' ' + forwarded_name_by[0]['p_last_name']
            forwarded_by.append(by_name)
            forwarded_to_ = approval['forwarded_to_id']
            forwarded_name_to = PEOPLE.objects.filter(id=forwarded_to_).values('p_first_name', 'p_last_name')
            to_name = forwarded_name_to[0]['p_first_name'] + ' ' + forwarded_name_to[0]['p_last_name']
            forwarded_to.append(to_name)
        approval_hierarchy = zip(approval_id, approval_level, type, project_id_id, forwarded_by, forwarded_to)
        project_name_ = PROJECT.objects.filter(id=project_id).values('project_name')
        project_name = project_name_[0]['project_name']
        context = {
            "approval_data": approval_data,
            "task_name": task_name,
            "project_name": project_name,
            "approval_hierarchy": approval_hierarchy
        }
        return render(request, 'task_workflow_in_task_summary.html', context)
    else:
        message = 'No approval hierarchy defined for "Support" task type. You are your own boss here.'
        return render(request, 'task_error_page.html', {'message': message})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


def home_approval_task(request):
    user_id = request.user.id
    p_id = UserForm.objects.filter(user_id=user_id).values('people_id')
    if p_id:
        ppl_id = p_id[0]['people_id']
        task_search = TASK.objects.all().filter(assigned_to_id=ppl_id)
        email = request.user.email
        people = PEOPLE.objects.filter(email_id=email).values('id')
        for i in people:
            id_ = i['id']
            task_approve_details = TASK_APPROVALS.objects.filter(forwarded_to_id=id_,
                                                                 approval_status='awaiting').values('id', 'task_id',
                                                                                                    'forwarded_by')
            t_id = []
            id_ = []
            forward_id = []
            p_id = []
            task_unique_id = []
            if task_approve_details:
                for i in task_approve_details:
                    seq_id = i['id']
                    id_.append(seq_id)
                    task_id = i['task_id']
                    task_list_val = TASK.objects.filter(id=task_id).values('task_name', 'project_id', 'id')
                    forwarded_by = i['forwarded_by']
                    email_id_ = PEOPLE.objects.filter(id=forwarded_by).values('email_id')
                    email = email_id_[0]['email_id']
                    forward_id.append(email)
                    # except:
                    #     messages.error(request, 'No user found!')
                    for i in task_list_val:
                        t_id.append(i['task_name'])
                        task_unique_id.append(i['id'])
                        project_table = PROJECT.objects.filter(id=i['project_id']).values('project_name')
                        p_id.append(project_table[0]['project_name'])
                    # if request.POST.get('forwarded_note'):
                    #     update_note =TASK_APPROVALS.objects.filter()
                list_val = zip(t_id, forward_id, p_id, id_, task_unique_id)
                context = {
                    'task_id': task_id,
                    'list_val': list_val,
                    'task_search': task_search
                }
                return render(request, 'approval_notification.html', context)
            # else:
            #     message = 'No data found.'
            #     return render(request, 'error_page.html', {'message': message})

        return render(request, 'approval_notification.html', {'task_search': task_search})
    else:
        message = 'You do not have sufficient privilages to show the details '
        return render(request, 'error_page.html', {'message': message})


def reject_approval_notification(request, pk):
    # user_details = get_object_or_404(TASK_APPROVALS, pk=pk)
    update_status = TASK_APPROVALS.objects.filter(id=pk).update(approval_status='rejected')
    search_task = TASK_APPROVALS.objects.filter(id=pk).values('task_id')
    update_task = TASK.objects.filter(id=search_task[0]['task_id']).update(approval_flag='Rejected')
    return redirect(f'/forwarded_note_{pk}')


def approval_notification_approved(request, pk):
    update_status = TASK_APPROVALS.objects.filter(id=pk).update(approval_status='approved')
    search_task = TASK_APPROVALS.objects.filter(id=pk).values('task_id', 'approval_level', 'forwarded_to_id')
    leval = search_task[0]['approval_level']
    search_project_id = TASK.objects.filter(id=search_task[0]['task_id']).values('project_id_id')
    project_id = search_project_id[0]['project_id_id']
    approval_hierachy = APPROVAL_HIERARCHY.objects.filter(project_id_id=project_id, approval_level__gt=leval).values(
        'approval_level', 'project_id_id', 'forwarded_to_id').order_by('approval_level')[:1]
    if approval_hierachy:
        hierachy_approval_leval = approval_hierachy[0]['approval_level']
        forwarded_to_id = approval_hierachy[0]['forwarded_to_id']
        create_task_approval = TASK_APPROVALS(approval_level=hierachy_approval_leval, executed='Yes',
                                              approval_status='awaiting',
                                              forwarded_by_id=search_task[0]['forwarded_to_id'],
                                              forwarded_to_id=forwarded_to_id, task_id_id=search_task[0]['task_id'])
        create_task_approval.save()
    else:
        update_task = TASK.objects.filter(id=search_task[0]['task_id']).update(approval_flag='Approved')
        try:
            if update_task:
                check_dba_processing = TASK.objects.filter(id=search_task[0]['task_id']).values('task_name',
                                'description','task_by','assigned_by','assigned_to','reassignable',
                                'status', 'parent_task', 'start_date','end_date','expected_end_date',
                                'task_type', 'required_dba_processing','project_id_id')
                for i in check_dba_processing:
                    if i['required_dba_processing'] is True:
                        task_name = 'DBA Processing' + ' ( ' + i['task_name'] + ' )'
                        description = 'DBA Processing' + ' ( ' + (i['description']) + ' )'
                        task_by = i['task_by']
                        assigned_by = i['assigned_by']
                        project = i['project_id_id']
                        parent_task = search_task[0]['task_id']
                        status = i['status']
                        today = date.today()
                        prjt_resrc = PROJECT_RESOURCES.objects.filter(project_id_id=project,
                                                                      resource_role='dba').values(
                            'resource_id').order_by('-id')[:1]
                        if prjt_resrc:
                            resource_id = prjt_resrc[0]['resource_id']
                            create_new_task = TASK(task_name=task_name, description=description,
                                                   task_by_id=task_by, assigned_by_id=assigned_by,
                                                   assigned_to_id=resource_id, reassignable=True, status=status,
                                                   start_date=today, task_type='Movement', parent_task_id=parent_task,
                                                   project_id_id=project,
                                                   created_by=user_login_fun(request),
                                                   last_updated_by=user_login_fun(request),
                                                   creation_date=datetime_functionality(), approval_flag='Approved',
                                                   last_update_date=datetime_functionality())
                            create_new_task.save()
                        else:
                            message = 'Task has been approved if you want DBA process ,Please select the role DBA in project resource firstly.'
                            return render(request, 'error_page.html', {'message': message})
        except:
            pass
    return redirect(f'/forwarded_note_{pk}')


def forwarded_note_view(request,pk):
    # if request.method == 'POST':
    form = TASK_APPROVALS_FORM(request.POST or None)
    if form.is_valid():
        form_1 = form.save(commit=False)
        forwarded_note = form.cleaned_data['forwarded_note']
        if forwarded_note:
            update_note = TASK_APPROVALS.objects.filter(id=pk).update(forwarded_note=forwarded_note)
        else:
            pass
        return redirect("/approvals_list")
    context = {
        'form': form,
    }
    return render(request, 'forwarded_note_update_from_notification.html', context)
    # else:
    #     form = TASK_APPROVALS_FORM()
    #     context = {
    #         'form': form,
    #     }
    #     return render(request, 'forwarded_note_update_from_notification.html', context)
    # if request.method == 'POST':
    #     form = TASK_APPROVALS_FORM(request.POST or None)
    #     if form.is_valid():
    #         form_1 = form.save(commit=False)
    #         forwarded_note = form.cleaned_data['forwarded_note']
    #         if forwarded_note:
    #             update_note = TASK_APPROVALS.objects.filter(id=pk).update(forwarded_note=forwarded_note)
    #         else:
    #             update_note = TASK_APPROVALS.objects.filter(id=pk).update(forwarded_note=None)
    #         return redirect("/approvals_list")
    #     context = {
    #         'form': form,
    #     }
    #     return render(request, 'forwarded_note_update_from_notification.html', context)
    # else:
    #     form = TASK_APPROVALS_FORM()
    #     context = {
    #         'form': form,
    #     }
    #     return render(request, 'forwarded_note_update_from_notification.html', context)
    # return redirect('/approvals_list')


def error(request):
    return render(request, 'error_page.html')


@login_required
def index(request):
    return redirect('/approvals_list')


def all_projects_list(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user_id = request.user.id
    p_id = UserForm.objects.filter(user_id=user_id).values_list('people_id')
    if p_id:
        for i in p_id:
            team_check_p_id = TEAM.objects.all().values('all_members', 'id')
            t_id = []
            for d in team_check_p_id:
                p_id_ = d['all_members']
                id = d['id']
                try:
                    if f'{i[0]}' in p_id_:
                        t_id.append(id)
                except:
                    pass
            team_id = str(t_id).replace('[', '(').replace(']', ')')
            # team_id =()
            project_resource = PROJECT_RESOURCES.objects.filter(
                Q(resource_id=i[0]) | Q(resource_id__in=team_id)).values('project_id_id')
            project_list = PROJECT.objects.all().filter(id__in=project_resource).order_by('-id')
            return render(request, 'project_list_view.html', {'project_list': project_list})
    else:
        pass


def show_owner(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    project = PROJECT.objects.filter(id=pk).values('project_name')
    owner_details = PROJECT_RESOURCES.objects.all().filter(project_id=pk, resource_role='owner').values('resource_id')
    first_name = []
    last_name = []
    # if owner_details:
    for j in owner_details:
        resource_id = j['resource_id']
        people_list_ = PEOPLE.objects.filter(id=resource_id).values('p_first_name', 'p_last_name')
        for p in people_list_:
            f_name = p['p_first_name']
            l_name = p['p_last_name']
            first_name.append(f_name)
            last_name.append(l_name)

    people_lists = zip(first_name, last_name)
    context = {
        'project': project,
        'people_lists': people_lists
    }
    return render(request, 'project_owner_details.html', context)


def parent_task_form_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    document = DOCUMENT.objects.filter(task_id=pk)
    task = TASK.objects.filter(id=pk)
    cursor = connection.cursor()
    task_details = f'''SELECT task_by_id, assigned_by_id,assigned_to_id
        FROM public.app_task where id='{pk}';
    '''
    cursor.execute(task_details)
    task_details_ = cursor.fetchall()
    for i in task_details_:
        assign_to_ = i[2],
        assign_by_ = i[1],
        task_by_ = i[0]
        assign_to_id = str(assign_to_).replace("(", '').replace(",)", '')
        assign_by_id = str(assign_by_).replace("(", '').replace(",)", '')
        task_by_id = str(task_by_).replace("(", '').replace(",)", '')
        assign_to = PEOPLE.objects.filter(id=assign_to_id).values('p_first_name', 'p_last_name')
        assign_by = PEOPLE.objects.filter(id=assign_by_id).values('p_first_name', 'p_last_name')
        task_by = PEOPLE.objects.filter(id=task_by_id).values('p_first_name', 'p_last_name')
        context = {
            "task": task,
            "document": document,
            "assign_to": assign_to,
            "assign_by": assign_by,
            "task_by": task_by

        }
        return render(request, 'parent_task_form_view.html', context)


def task_details_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    document = DOCUMENT.objects.filter(task_id=pk)
    task = TASK.objects.filter(id=pk)
    cursor = connection.cursor()
    task_details = f'''SELECT task_by_id, assigned_by_id,assigned_to_id
        FROM public.app_task where id='{pk}';
    '''
    cursor.execute(task_details)
    task_details_ = cursor.fetchall()
    for i in task_details_:
        assign_to_ = i[2],
        assign_by_ = i[1],
        task_by_ = i[0]
        assign_to_id = str(assign_to_).replace("(", '').replace(",)", '')
        assign_by_id = str(assign_by_).replace("(", '').replace(",)", '')
        task_by_id = str(task_by_).replace("(", '').replace(",)", '')
        assign_to = PEOPLE.objects.filter(id=assign_to_id).values('p_first_name', 'p_last_name')
        assign_by = PEOPLE.objects.filter(id=assign_by_id).values('p_first_name', 'p_last_name')
        task_by = PEOPLE.objects.filter(id=task_by_id).values('p_first_name', 'p_last_name')
        context = {
            "task": task,
            "document": document,
            "assign_to": assign_to,
            "assign_by": assign_by,
            "task_by": task_by

        }
        return render(request, 'task_details_form_view.html', context)


def all_people_list(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    people_list = PEOPLE.objects.all().order_by('-id')
    return render(request, 'people_list_view.html', {'people_list': people_list})


def all_application_list(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    application_list = APPLICATION.objects.all().order_by('-id')
    return render(request, 'application_list_view.html', {'application_list': application_list})


def project_all_task_list(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    project_resrc = PROJECT_RESOURCES.objects.filter(project_id=pk).values('resource_id', 'resource_role')
    first_name = []
    last_name = []
    email = []
    contact = []
    resource_role_ = []
    for i in project_resrc:
        resource_role = i['resource_role']
        resource_id = i['resource_id']
        people_list_ = PEOPLE.objects.filter(id=resource_id).values('p_first_name', 'p_last_name', 'email_id',
                                                                    'contact_no')
        resource_role_.append(resource_role)
        for p in people_list_:
            f_name = p['p_first_name']
            l_name = p['p_last_name']
            email_id = p['email_id']
            contact_no = p['contact_no']
            first_name.append(f_name)
            last_name.append(l_name)
            contact.append(contact_no)
            email.append(email_id)
    people_list = zip(first_name, last_name, email, contact, resource_role_)
    # people_list =TASK.objects.filter(project_id=pk).values('assigned_to_id')
    # people_list =PEOPLE.objects.filter(id__in=task_db)
    # task_list = TASK.objects.all().filter(project_id=pk).order_by('-id')
    project_list = PROJECT.objects.all().filter(id=pk).order_by('-id')
    cursor = connection.cursor()
    activity_date = f'''SELECT last_update_date FROM public.app_task where
     project_id_id = '{pk}' order by last_update_date desc limit 1;
    '''
    cursor.execute(activity_date)
    l_activity_Date = cursor.fetchall()
    last_activity_Date = str(l_activity_Date).replace("[('", '').replace("',)]", '')
    # last_activity_Date = TASK.objects.all().filter(project_id=pk).values('last_update_date').order_by('-last_update_date')[:1]
    task_list = TASK.objects.all().filter(project_id=pk).values('id', 'task_name',
                                                                'task_by_id', 'assigned_by_id', 'assigned_to_id',
                                                                'status', 'reassignable', 'start_date', 'end_date',
                                                                'expected_end_date', 'task_type',
                                                                'task_complete','initial_expected_end_date').order_by('-id')
    id_ = []
    task_name = []
    task_by_f_name = []
    task_by_l_name = []
    assign_by_f_name = []
    assign_by_l_name = []
    assign_to_l_name = []
    assign_to_f_name = []
    status = []
    initial_expected_end_date=[]
    start_date = []
    reassignable = []
    end_date = []
    expected_end_date = []
    task_type = []
    task_complete = []

    for i in task_list:
        id = i['id']
        t_name = i['task_name']
        status_ = i['status']
        s_date = i['start_date']
        task_complt = i['task_complete']
        e_date = i['end_date']
        e_e_date = i['expected_end_date']
        t_type = i['task_type']
        initial_expected_end_date_ = i['initial_expected_end_date']
        task_by_ = i['task_by_id']
        assign_by_ = i['assigned_by_id']
        assign_to_ = i['assigned_to_id']
        assign_to_id = str(assign_to_).replace("(", '').replace(",)", '')
        assign_by_id = str(assign_by_).replace("(", '').replace(",)", '')
        task_by_id = str(task_by_).replace("(", '').replace(",)", '')
        assign_to = PEOPLE.objects.filter(id=assign_to_id).values('p_first_name', 'p_last_name')
        assign_by = PEOPLE.objects.filter(id=assign_by_id).values('p_first_name', 'p_last_name')
        task_by = PEOPLE.objects.filter(id=task_by_id).values('p_first_name', 'p_last_name')
        for t_by in task_by:
            task_by_f_name.append(t_by['p_first_name'])
            task_by_l_name.append(t_by['p_last_name'])
        for a_by in assign_by:
            assign_by_f_name.append(a_by['p_first_name'])
            assign_by_l_name.append(a_by['p_last_name'])
        for a_to in assign_to:
            assign_to_f_name.append(a_to['p_first_name'])
            assign_to_l_name.append(a_to['p_last_name'])
        re_assignable = i['reassignable']
        id_.append(id)
        task_name.append(t_name)
        task_type.append(t_type)
        initial_expected_end_date.append(initial_expected_end_date_)
        expected_end_date.append(e_e_date)
        reassignable.append(re_assignable)
        end_date.append(e_date)
        start_date.append(s_date)
        status.append(status_)
        task_complete.append(task_complt)
    task_list_ = zip(id_, task_name, status, start_date, end_date, expected_end_date, task_type, reassignable,
                     task_by_f_name, task_by_l_name, assign_by_f_name, assign_by_l_name, assign_to_f_name,
                     assign_to_l_name, task_complete,initial_expected_end_date)
    context = {'task_list': task_list_,
               'project_list': project_list,
               'people_list': people_list,
               # 'assign_to': assign_to,
               'pk': pk,
               'id_': id_,
               # 'task_people': task_people,
               'last_activity_Date': last_activity_Date,
               # 'task_by': task_by
               }
    return render(request, 'project_all_task_view.html', context)


def complete_task_process(request, pk):
    user_id_ = request.user.id
    userform = UserForm.objects.filter(user_id=user_id_).values('people_id')
    p_id = userform[0]['people_id']
    cursor = connection.cursor()
    task_form = f'''
    SELECT project_id_id
    FROM public.app_task where id = '{pk}' and (assigned_by_id='{p_id}' or assigned_to_id='{p_id}');
    '''
    cursor.execute(task_form)
    task_data = cursor.fetchall()

    if task_data:
        project_id = str(task_data).replace('[(', '').replace(',)]', '')
        update_task = TASK.objects.filter(id=pk).update(task_complete=True)
        return redirect(f'/all_task_list_{project_id}')
    else:
        message = "You do not have enough privilages to complete this task." + '\n' + 'you should be either an assigner' \
                                                                                      ' or assignee to complete this task'
        return render(request, 'error_page.html', {'message': message})


def task_form_view_from_all_task(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user_id = request.user.id
    user_form = UserForm.objects.filter(user_id=user_id).values('people_id')
    if user_form:
        people_id = user_form[0]['people_id']
        project_model = PROJECT.objects.filter(id=pk).values_list('task_creation', 'project_name')
        project_name = project_model[0][1]
        task_project= TASK.objects.filter(project_id_id=pk)
        if project_model[0][0] == 'self':
            form = TASK_FORM1(request.POST or None)
            if form.is_valid():
                form_1 = form.save(commit=False)
                project_id = pk
                request.session['project_id'] = project_id
                # task_by = form.cleaned_data['task_by']
                task_name = form.cleaned_data['task_name']
                description = form.cleaned_data['description']
                assigned_by = form.cleaned_data['assigned_by']
                assigned_to = form.cleaned_data['assigned_to']
                required_dba_processing = form.cleaned_data['required_dba_processing']
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                expected_end_date = form.cleaned_data['expected_end_date']
                task_type = form.cleaned_data['task_type']
                status = form.cleaned_data['status']
                reassignable = form.cleaned_data['reassignable']
                parent_task = request.POST.get("parent_task")
                if task_type == 'support':
                    approval_flag = 'Not Required'
                else:
                    approval_flag = 'on_going'
                try:
                    if parent_task:
                        p_task_id =TASK.objects.filter(task_name=parent_task).values('id')
                        parent_task = p_task_id[0]['id']
                except:
                    parent_task = None
                try:
                    assigned_to = assigned_to.id
                except:
                    assigned_to = None
                try:
                    assigned_by = assigned_by.id
                except:
                    assigned_by = None
                # try:
                #     task_by = task_by.id
                # except:
                #     task_by = None
                if start_date > end_date or start_date > expected_end_date:
                    messages.error(request, 'Expected/End date must be equal or greater than to start date')
                elif end_date < expected_end_date:
                    messages.error(request, 'Expected End date must be equal or less than to end date ')
                else:
                    task_table_save = TASK(project_id_id=pk, task_name=task_name, task_by_id=people_id,
                                           assigned_by_id=assigned_by, assigned_to_id=assigned_to,initial_expected_end_date=end_date,
                                           start_date=start_date, end_date=end_date, description=description,
                                           status=status, reassignable=reassignable, parent_task_id=parent_task,
                                           created_by=user_login_fun(request), last_updated_by=user_login_fun(request),
                                           creation_date=datetime_functionality(), expected_end_date=expected_end_date,
                                           last_update_date=datetime_functionality(), task_type=task_type,
                                           approval_flag=approval_flag, required_dba_processing=required_dba_processing)
                    task_table_save.save()
                    table_task = task_table_save.id
                    id_ = ''.join(c for c in str(table_task) if c.isdigit())
                    request.session['id_'] = id_
                    data = TASK.objects.filter(id=id_).values('approval_flag', 'project_id_id')
                    # Approval Login
                    if data[0]['approval_flag'] == 'on_going':
                        approval_hierarchy = APPROVAL_HIERARCHY.objects.filter(project_id_id=data[0]['project_id_id'],
                                                                               approval_level='1').values('approval_level',
                                                                                                          'forwarded_to')
                        if approval_hierarchy:
                            forwarded_to = approval_hierarchy[0]['forwarded_to']
                            approval_level = approval_hierarchy[0]['approval_level']
                            user_id_ = request.user.id
                            userform = UserForm.objects.filter(user_id=user_id_).values('people_id')
                            if userform:
                                p_id = userform[0]['people_id']
                                cursor = connection.cursor()
                                approval_task = f'''
                                INSERT INTO public.app_task_approvals(
                                    approval_level, executed, approval_status, forwarded_by_id, forwarded_to_id, task_id_id)
                                    VALUES ('{approval_level}', 'Yes','awaiting',{p_id} , {forwarded_to}, {id_});
                                '''
                                cursor.execute(approval_task)
                    return redirect(f"/document_{pk}")
            return render(request, 'task_form_view_from_all_task_list.html', {'form': form, 'project_name': project_name,
                                                                              'task_project':task_project})
        else:
            if project_model[0][0] == 'owner':
                user_id = request.user.id
                user_form = UserForm.objects.filter(user_id=user_id).values('people_id')
                if user_form:
                    project_resrc = PROJECT_RESOURCES.objects.filter(project_id=pk, resource_role='owner').values(
                        'resource_id')
                    if project_resrc:
                        if project_resrc[0]['resource_id'] == user_form[0]['people_id']:
                            form = TASK_FORM1(request.POST or None)
                            if form.is_valid():
                                form_1 = form.save(commit=False)
                                project_id = pk
                                request.session['project_id'] = project_id
                                # task_by = form.cleaned_data['task_by']
                                task_name = form.cleaned_data['task_name']
                                description = form.cleaned_data['description']
                                assigned_by = form.cleaned_data['assigned_by']
                                assigned_to = form.cleaned_data['assigned_to']
                                start_date = form.cleaned_data['start_date']
                                end_date = form.cleaned_data['end_date']
                                expected_end_date = form.cleaned_data['expected_end_date']
                                status = form.cleaned_data['status']
                                reassignable = form.cleaned_data['reassignable']
                                required_dba_processing = form.cleaned_data['required_dba_processing']
                                parent_task = request.POST.get("parent_task")
                                task_type = form.cleaned_data['task_type']
                                if task_type == 'support':
                                    approval_flag = 'Not Required'
                                else:
                                    approval_flag = 'on_going'
                                try:
                                    if parent_task:
                                        p_task_id = TASK.objects.filter(task_name=parent_task).values('id')
                                        parent_task = p_task_id[0]['id']
                                except:
                                    parent_task = None
                                if start_date > end_date or start_date > expected_end_date:
                                    messages.error(request,
                                                   'Expected/End date must be equal or greater than to start date')
                                elif end_date < expected_end_date:
                                    messages.error(request, 'Expected End date must be equal or less than to end date ')
                                else:
                                    task_table_save = TASK(project_id_id=project_id, task_name=task_name, task_by_id=people_id,
                                                           assigned_by_id=assigned_by.id, assigned_to_id=assigned_to.id,
                                                           start_date=start_date, end_date=end_date, description=description,
                                                           status=status, reassignable=reassignable, parent_task_id=parent_task,
                                                           created_by=user_login_fun(request),initial_expected_end_date=end_date,
                                                           last_updated_by=user_login_fun(request),
                                                           creation_date=datetime_functionality(),
                                                           expected_end_date=expected_end_date,
                                                           last_update_date=datetime_functionality(), task_type=task_type,
                                                           approval_flag=approval_flag,
                                                           required_dba_processing=required_dba_processing
                                                           )
                                    task_table_save.save()
                                    table_task = task_table_save.id
                                    id_ = ''.join(c for c in str(table_task) if c.isdigit())
                                    request.session['id_'] = id_
                                    data = TASK.objects.filter(id=id_).values('approval_flag', 'project_id_id')
                                    if data[0]['approval_flag'] == 'on_going':
                                        approval_hierarchy = APPROVAL_HIERARCHY.objects.filter(
                                            project_id_id=data[0]['project_id_id'],
                                            approval_level='1').values('approval_level', 'forwarded_to')
                                        if approval_hierarchy:
                                            forwarded_to = approval_hierarchy[0]['forwarded_to']
                                            approval_level = approval_hierarchy[0]['approval_level']

                                            user_id_ = request.user.id
                                            userform = UserForm.objects.filter(user_id=user_id_).values('people_id')
                                            if userform:
                                                p_id = userform[0]['people_id']
                                                cursor = connection.cursor()
                                                approval_task = f'''
                                              INSERT INTO public.app_task_approvals(
                                              approval_level, executed, approval_status, forwarded_by_id, forwarded_to_id, task_id_id)
                                              VALUES ('{approval_level}', 'Yes','awaiting',{p_id} , {forwarded_to}, {id_});
                                              '''
                                                cursor.execute(approval_task)
                                    return redirect(f"/document_{pk}")
                            return render(request, 'task_form_view_from_all_task_list.html',
                                          {'form': form, 'project_name': project_name,'task_project':task_project})
                        else:
                            message = 'You do not have sufficient privileges to create this task!'
                            return render(request, 'error_page.html', {'message': message})
                    else:
                        message = 'You do not have sufficient privileges to create this task!'
                        return render(request, 'error_page.html', {'message': message})
                else:
                    message = 'You do not have sufficient privileges to create this task!'
                    return render(request, 'error_page.html', {'message': message})
    else:
        message = "Please create the user details firstly"
    return render(request, 'error_page.html', {'message': message})


def edit_task_form(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user_id = request.user.id
    user_form = UserForm.objects.filter(user_id=user_id).values('people_id')
    if user_form:
        p_id = user_form[0]['people_id']
        edit_task = TASK.objects.filter(id=kwargs['pk']).values('approval_flag', 'task_by','assigned_by','assigned_to')
        if edit_task[0]['approval_flag'] == 'Approved' or edit_task[0]['approval_flag'] == 'on_going':
            message = 'You do not have sufficient privilages to edit this task'
            return render(request, 'error_page.html', {'message': message})
        else:
            if p_id== f"{edit_task[0]['task_by']}" or (p_id== f"{edit_task[0]['assigned_by']}" or p_id== f"{edit_task[0]['assigned_to']}"):
                new_item = get_object_or_404(TASK, pk=kwargs['pk'])
                queryset = TASK.objects.select_related().filter(pk=kwargs['pk'])
                project_name = []
                for i in queryset:
                    project_val = i.project_id
                    project_name.append(project_val)
                    data = queryset.update(
                        assigned_by_id=i.assigned_by, assigned_to_id=i.assigned_to,
                        start_date=i.start_date, end_date=i.end_date, expected_end_date=i.expected_end_date,
                        status=i.status, reassignable=i.reassignable, parent_task_id=i.parent_task,
                        last_update_date=last_update_fun(), task_name=i.task_name)
                form = TASK_EDIT_FORM(request.POST or None, instance=new_item)
                if form.is_valid():
                    form_data = form.save(commit=False)
                    form_data.save()
                    return redirect(f"/document_{kwargs['pk']}")
                context = {
                    "project_name": project_name,
                    "form": form,
                }
                return render(request, "edit_task_form_view.html", context)
            else:
                message = 'You do not have sufficient privilages to edit this task '
                return render(request, 'error_page.html', {'message': message})
    else:
        message = 'You do not have sufficient privilages to edit this task '
        return render(request, 'error_page.html', {'message': message})



def document_form_upload_from_task_list(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # id_ = '22'
    id_ = request.session.get('id_')
    project_id = request.session.get('project_id')
    if id_ and project_id:
        if request.method == 'POST':
            form = DOCUMENT_FORM(request.POST, request.FILES)
            if form.is_valid():
                form1 = form.save(commit=False)
                document_name = form.cleaned_data['document_name']
                document_type = form.cleaned_data['document_type']
                document_location = form.cleaned_data['document_location']
                create_doc = DOCUMENT(document_name=document_name, document_location=document_location,
                                      document_type=document_type,
                                      task_id=id_, project_id=project_id, creation_date=datetime_functionality(),
                                      last_update_date=datetime_functionality(), created_by=user_login_fun(request),
                                      last_updated_by=user_login_fun(request))
                create_doc.save()
                return redirect(f"/document_{pk}")
        else:
            form = DOCUMENT_FORM()
    else:
        message = 'Please Create the task firstly'
        return render(request, 'error_page.html', {'message': message})

    photos_list = DOCUMENT.objects.all().filter(task_id=id_)
    context = {
        'form': form,
        'photos_list': photos_list,
        'id': id_,
        'pk': pk,
        'project_id': project_id
    }
    return render(request, 'doc_form_view_from_all_task.html', context)


def project_resource_individual_from_all_task_list(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    project = PROJECT.objects.filter(id=pk).values_list('project_name', flat=True)
    form = PROJECT_RESOURCES_FORM(request.POST or None)
    if form.is_valid():
        form_1 = form.save(commit=False)
        resource_pool = 'individual'
        resource_role = form.cleaned_data['resource_role']
        individual_resource_id = form.cleaned_data['individual_resource_id']
        try:
            resource_id = individual_resource_id.id
        except:
            resource_id = None
        if resource_role == 'owner':
            p_resource = PROJECT_RESOURCES.objects.filter(project_id=pk, resource_role='owner')
            if not p_resource:
                project_resource_table = PROJECT_RESOURCES(project_id_id=pk, resource_id=resource_id,
                                                           resource_pool=resource_pool, resource_role=resource_role,
                                                           created_by=user_login_fun(request),
                                                           last_updated_by=user_login_fun(request),
                                                           creation_date=datetime_functionality(),
                                                           last_update_date=datetime_functionality())
                project_resource_table.save()
                return redirect(f'/individual_resource_{pk}')
            else:
                message = 'The project owner is selected ..please try with another role!!'
                return render(request, 'error_page.html', {'message': message})
        else:
            project_resource_table = PROJECT_RESOURCES(project_id_id=pk, resource_id=resource_id,
                                                       resource_pool=resource_pool, resource_role=resource_role,
                                                       created_by=user_login_fun(request),
                                                       last_updated_by=user_login_fun(request),
                                                       creation_date=datetime_functionality(),
                                                       last_update_date=datetime_functionality())
            project_resource_table.save()
            return redirect(f'/individual_resource_{pk}')
    return render(request, 'project_resource_from_all_task.html', {'form': form, 'project': project, 'pk': pk})


def project_resource_team_from_all_task(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    project = PROJECT.objects.filter(id=pk).values_list('project_name', flat=True)
    form = PROJECT_RESOURCES_TEAM_FORM(request.POST or None)
    if form.is_valid():
        resource_pool = 'team'
        team_resource_role = form.cleaned_data['team_resource_role']
        team_resource_id = form.cleaned_data['team_resource_id']
        resource_id = team_resource_id.id
        project_resource_table = PROJECT_RESOURCES(project_id_id=pk, resource_id=resource_id,
                                                   resource_pool=resource_pool, resource_role=team_resource_role,
                                                   created_by=user_login_fun(request),
                                                   last_updated_by=user_login_fun(request),
                                                   creation_date=datetime_functionality(),
                                                   last_update_date=datetime_functionality()
                                                   )
        project_resource_table.save()
        return redirect(f'/team_resource_{pk}')
    return render(request, 'project_resource_team_from_all_task.html', {'form': form, 'project': project, 'pk': pk})
    # if request.method == 'GET':
    #     query = request.GET.get('q')
    #     if query:
    #         task_list = TASK.objects.filter(Q(task_name__istartswith=query) | Q(description__istartswith=query)
    #                                         | Q(parent_task_id__istartswith=query) | Q(start_date__istartswith=query)
    #                                         | Q(expected_end_date__istartswith=query) | Q(status__istartswith=query)
    #                                         | Q(reassignable__istartswith=query))
    #         if task_list:
    #             return render(request, 'task_list_view.html', {'task_list': task_list,'project_list':project_list})
    #         else:
    #             return JsonResponse({'Message': "No Data Found with this Search !!!"})
    #     else:
    #         task_list = TASK.objects.all().filter(project_id=pk).order_by('-id')


def user_login_fun(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        return user_id
    else:
        user_name = 'AnonymousUser'
        return user_name


def datetime_functionality():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d %I-%M-%S %p")
    return current_date


def last_update_fun():
    now = datetime.now()
    update_date = now.strftime("%Y-%m-%d %I-%M-%S %p")
    return update_date


class PEOPLE_FORM_VIEW(TemplateView):
    '''
    people form view
    '''
    form_class = PEOPLE_FORM
    form_1 = None

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_id = request.user.id
        user_form = UserForm.objects.filter(user_id=user_id).values('people_id')
        if user_form:
            people_table_check = PEOPLE.objects.filter(id=user_form[0]['people_id']).values('can_create_people')
            if people_table_check[0]['can_create_people'] is True:
                self.form_1 = self.form_class(prefix='form_1')
            else:
                message = 'You do not have sufficient privileges to add new user!'
                return render(request, 'error_page.html', {'message': message})
        else:
            message = 'The User has no people id'
            return render(request, 'error_page.html', {'message': message})

        return super(PEOPLE_FORM_VIEW, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        user_form = UserForm.objects.filter(user_id=user_id).values('people_id')
        if user_form:
            people_table_check = PEOPLE.objects.filter(id=user_form[0]['people_id']).values('can_create_people')
            if people_table_check[0]['can_create_people'] is True:
                self.form_1 = self.form_class(prefix='form_1', data=request.POST)
                if self.form_1.is_valid():
                    form_db = self.form_1.save(commit=False)
                    p_first_name = self.form_1.cleaned_data['p_first_name']
                    p_last_name = self.form_1.cleaned_data['p_last_name']
                    email_id = self.form_1.cleaned_data['email_id']
                    contact_no = self.form_1.cleaned_data['contact_no']
                    department = self.form_1.cleaned_data['department']
                    can_create_project = self.form_1.cleaned_data['can_create_project']
                    can_create_people = self.form_1.cleaned_data['can_create_people']
                    can_create_application = self.form_1.cleaned_data['can_create_application']
                    people_table = PEOPLE(p_first_name=p_first_name, p_last_name=p_last_name,
                                          can_create_people=can_create_people,
                                          can_create_application=can_create_application, can_create_project=can_create_project,
                                          email_id=email_id, contact_no=contact_no, created_by=user_login_fun(request),
                                          department=department, last_updated_by=user_login_fun(request),
                                          creation_date=datetime_functionality(), last_update_date=datetime_functionality())
                    people_table.save()
                    return redirect(f'/signup_{people_table.id}')
                else:
                    message =self.form_1.errors
                    return render(request, 'error_page.html', {'message': message})
            else:
                message = 'You do not have sufficient privileges to add new user!'
                return render(request, 'error_page.html', {'message': message})
        else:
            message = 'The User has no people id'
            return render(request, 'error_page.html', {'message': message})


    def get_context_data(self, **kwargs):
        context = super(PEOPLE_FORM_VIEW, self).get_context_data(**kwargs)
        context['form_1'] = self.form_1
        return context


class PEOPLE_FORM_DATA(PEOPLE_FORM_VIEW):
    '''
    calling process of people form view
    '''
    template_name = 'people_form_view.html'

    def __init__(self, *args, **kwargs):
        # For this case we must set DJANGO_POPUP_VIEW_FIELD_TEMPLATE_PACK
        settings.DJANGO_POPUP_VIEW_FIELD_TEMPLATE_PACK = 'bootstrap3'
        super(PEOPLE_FORM_DATA, self).__init__(*args, **kwargs)


def signup(request, pk):
    user_detail = PEOPLE.objects.filter(id=pk).values_list('p_first_name', 'p_last_name', 'email_id')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.is_staff = True
            first_name = user_detail[0][0]
            last_name = user_detail[0][1]
            email = user_detail[0][2]
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            cursor = connection.cursor()
            user_form_create = f'''
            INSERT INTO public.app_userform(
            user_id, people_id)
            VALUES ({user.id}, {pk});'''
            cursor.execute(user_form_create)
            # login(request, user)
            return redirect('/people')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def edit_people_form(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user_id = request.user.id
    user_form = UserForm.objects.filter(user_id=user_id).values('people_id')
    if user_form:
        people_table_check = PEOPLE.objects.filter(id=user_form[0]['people_id']).values('can_create_people')
        if people_table_check[0]['can_create_people'] is True:
            new_item = get_object_or_404(PEOPLE, pk=kwargs['pk'])
            queryset = PEOPLE.objects.select_related().filter(pk=kwargs['pk'])
            for i in queryset:
                data = queryset.update(p_first_name=i.p_first_name, p_last_name=i.p_last_name,
                                       email_id=i.email_id, contact_no=i.contact_no,
                                       department=i.department, last_update_date=last_update_fun())
            form = PEOPLE_FORM(request.POST or None, instance=new_item)
            if form.is_valid():
                form_data = form.save(commit=False)
                form_data.save()
                return redirect('/all_people_list')
            context = {
                "form": form,
            }
            return render(request, "update_people_form_view.html", context)
        else:
            message = 'You do not have sufficient privileges to edit people and permissions.'
            return render(request, 'error_page.html', {'message': message})
    else:
        message = 'The User has no people id'
        return render(request, 'error_page.html', {'message': message})


def team_view_1(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    form = TEAM_FORM1(request.POST or None)
    if form.is_valid():
        form_1 = form.save(commit=False)
        team_name = form.cleaned_data['team_name']
        team_description = form.cleaned_data['team_description']
        request.session['team_name'] = team_name
        request.session['team_description'] = team_description
        return redirect('/team_add')
    return render(request, 'team_view_form1.html', {'form': form})


def team_view_2(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    form = TEAM_FORM2(request.POST or None)
    team_name = request.session.get('team_name')
    team_description = request.session.get('team_description')
    cursor = connection.cursor()
    team_name_find = f'''SELECT id, team_id, team_name, 
                           team_description, creation_date, last_update_date, created_by,
                           last_updated_by, active, segment_1, segment_2, segment_3, segment_4, 
                           segment_5, team_member_id, all_members
                           FROM public.app_team where team_name='{team_name}' 
                           and team_description='{team_description}';
                           '''
    cursor.execute(team_name_find)
    queryset = cursor.fetchall()
    if form.is_valid():
        form_1 = form.save(commit=False)
        team_member_id = form.cleaned_data['team_member']
        if queryset:
            for i in queryset:
                id = i[0]
                all_member = [f'{i[15]}']
                memberid = [f'{team_member_id.id}']
                all_member.extend(memberid)
                update_members = str(all_member).replace("'", '').replace('[', '').replace(']', '')
                final_query_ = list(update_members.split(','))
                final_query = [x.strip(' ') for x in final_query_]
                for i in final_query:
                    if final_query.count(i) > 1:
                        final_query.remove(i)
                final_queries = [i for i in final_query if i != '0']

                update_members_team = str(final_queries).replace("'", "").replace('[', '').replace(']', '')
                update_row_member = f'''
                                UPDATE public.app_team
                 SET all_members = '{update_members_team}' , last_update_date='{last_update_fun()}'
                                    WHERE id = '{id}';
                                                '''
                cursor.execute(update_row_member)
            return redirect('/team_add')
        elif not queryset:
            team_table_save = TEAM(team_name=team_name, team_description=team_description,
                                   all_members=team_member_id.id, created_by=user_login_fun(request),
                                   last_updated_by=user_login_fun(request), creation_date=datetime_functionality(),
                                   last_update_date=datetime_functionality())
            team_table_save.save()
            return redirect('/team_add')
    cursor = connection.cursor()
    team_members_ = f'''SELECT DISTINCT  all_members
                              FROM public.app_team where team_name='{team_name}' 
                   and team_description='{team_description}';
                      '''
    cursor.execute(team_members_)
    all_mem = cursor.fetchall()
    all_list_data = str(all_mem).replace("'", '').replace('[(', '').replace(',)]', '')
    try:
        model_data = PEOPLE.objects.filter(id__in=list(all_list_data.split(",")))
    except:
        model_data = []
    context = {
        "form": form,
        'model_data': model_data,
        'team_name': team_name,
        'team_description': team_description,
    }
    return render(request, "team_form_view.html", context)


# def edit_team_form(request, **kwargs):
#     new_item = get_object_or_404(PEOPLE,  pk=kwargs['pk'])
#     queryset = TEAM.objects.select_related().filter(pk=kwargs['pk'])
#     for i in queryset:
#         data = queryset.update(team_name=i.team_name,team_description=i.team_description,
#                                team_member_id=i.team_member_id.id,
#                                last_update_date=last_update_fun()
#                                )
#     form = TEAM_FORM1(request.POST or None, instance=new_item)
#     if form.is_valid():
#         form_data = form.save(commit=False)
#         form_data.save()
#         return redirect('/people')
#     context = {
#         "form": form,
#     }
#     return render(request, "update_team_form_view.html", context)


def task_form_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    form = TASK_FORM(request.POST or None)
    if form.is_valid():
        form_1 = form.save(commit=False)
        project_id = form.cleaned_data['project_id']
        request.session['project_id'] = project_id.id
        task_by = form.cleaned_data['task_by']
        task_name = form.cleaned_data['task_name']
        description = form.cleaned_data['description']
        assigned_by = form.cleaned_data['assigned_by']
        assigned_to = form.cleaned_data['assigned_to']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        expected_end_date = form.cleaned_data['expected_end_date']
        task_type = form.cleaned_data['task_type']
        status = form.cleaned_data['status']
        reassignable = form.cleaned_data['reassignable']
        parent_task = form.cleaned_data['parent_task']
        if task_type == 'support':
            approval_flag = 'na'
        else:
            approval_flag = 'on_going'
        try:
            parent_task = parent_task.id
        except:
            parent_task = None
        task_table_save = TASK(project_id_id=project_id.id, task_name=task_name, task_by_id=task_by.id,
                               assigned_by_id=assigned_by.id, assigned_to_id=assigned_to.id,
                               start_date=start_date, end_date=end_date, description=description,
                               status=status, reassignable=reassignable, parent_task_id=parent_task,
                               created_by=user_login_fun(request), last_updated_by=user_login_fun(request),
                               creation_date=datetime_functionality(), expected_end_date=expected_end_date,
                               last_update_date=datetime_functionality(), task_type=task_type,
                               approval_flag=approval_flag
                               )
        task_table_save.save()
        table_task = task_table_save.id
        id_ = ''.join(c for c in str(table_task) if c.isdigit())
        request.session['id_'] = id_
        return redirect("/document")
    else:
        return render(request, 'task_form_view.html', {'form': form})


def document_form_upload(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # id_ = '22'
    id_ = request.session.get('id_')
    project_id = request.session.get('project_id')
    if id_ and project_id:
        if request.method == 'POST':
            form = DOCUMENT_FORM(request.POST, request.FILES)
            if form.is_valid():
                form1 = form.save(commit=False)
                document_name = form.cleaned_data['document_name']
                document_location = form.cleaned_data['document_location']
                create_doc = DOCUMENT(document_name=document_name, document_location=document_location,
                                      task_id=id_, project_id=project_id, creation_date=datetime_functionality(),
                                      last_update_date=datetime_functionality(), created_by=user_login_fun(request),
                                      last_updated_by=user_login_fun(request))
                create_doc.save()
                return redirect(f"/document")
        else:
            form = DOCUMENT_FORM()
    else:
        message = 'Please Create the task firstly'
        return render(request, 'error_page.html', {'message': message})

    photos_list = DOCUMENT.objects.all().filter(task_id=id_)
    context = {
        'form': form,
        'photos_list': photos_list,
        'id': id_,
        'project_id': project_id
    }
    return render(request, 'doc_form_view.html', context)




def project_form_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user_id = request.user.id
    try:
        user_form = UserForm.objects.filter(user_id=user_id).values('people_id')
        if user_form:
            people_table_check = PEOPLE.objects.filter(id=user_form[0]['people_id']).values('can_create_project')
            if people_table_check[0]['can_create_project'] is True:
                form = PROJET_FORM(request.POST or None)
                if form.is_valid():
                    form_1 = form.save(commit=False)
                    project_name = form.cleaned_data['project_name']
                    user_id = request.user
                    application_id = form.cleaned_data['application_id']
                    try:
                        application_id = application_id.id
                    except:
                        application_id = None
                    project_type = form.cleaned_data['project_type']
                    project_description = form.cleaned_data['project_description']
                    start_date = form.cleaned_data['start_date']
                    expected_end_date = form.cleaned_data['expected_end_date']
                    status = form.cleaned_data['status']
                    task_creation = form.cleaned_data['task_creation']
                    project_business_owner = form.cleaned_data['project_business_owner']
                    project_objective = form.cleaned_data['project_objective']
                    self_task_reasignment = form.cleaned_data['self_task_reasignment']
                    if start_date > expected_end_date:
                        messages.error(request, 'Expected End date must be equal or greater than to start date')
                    else:
                        project_table_save = PROJECT(project_name=project_name, application_id_id=application_id,
                                                     project_description=project_description, project_type=project_type,
                                                     start_date=start_date, expected_end_date=expected_end_date,
                                                     status=status, task_creation=task_creation,initial_exp_completion_dt=expected_end_date,
                                                     login_create_user=user_id,
                                                     self_task_reasignment=self_task_reasignment,
                                                     project_business_owner=project_business_owner,
                                                     created_by=user_login_fun(request),
                                                     last_updated_by=user_login_fun(request),
                                                     creation_date=datetime_functionality(),
                                                     project_objective=project_objective,
                                                     last_update_date=datetime_functionality()
                                                     )
                        project_table_save.save()
                        table_task = project_table_save.id
                        id_ = ''.join(c for c in str(table_task) if c.isdigit())
                        user = request.user.id
                        people_id = UserForm.objects.filter(user_id=user).values('people_id')[:1]
                        p_id = people_id[0]['people_id']
                        project_resource = PROJECT_RESOURCES(project_id_id=id_, resource_pool='individual',
                                                             resource_role='Creator', resource_id=p_id,
                                                             created_by=user_login_fun(request),
                                                             last_updated_by=user_login_fun(request),
                                                             creation_date=datetime_functionality(),
                                                             last_update_date=datetime_functionality()
                                                             )
                        project_resource.save()
                        return redirect('/project')
            else:
                message = 'You do not have sufficient privileges to create the project!'
                return render(request, 'error_page.html', {'message': message})
    except:
        message = 'To create the project, should have  user id in user form'
        return render(request, 'error_page.html', {'message': message})

    return render(request, 'project_form_view.html', {'form': form})


def edit_project_form(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    project_id = kwargs['pk']
    new_item = get_object_or_404(PROJECT, pk=kwargs['pk'])
    queryset = PROJECT.objects.select_related().filter(pk=kwargs['pk'])
    for i in queryset:
        data = queryset.update(project_type=i.project_type, expected_end_date=i.expected_end_date,
                               project_description=i.project_description, status=i.status,
                               task_creation=i.task_creation,
                               self_task_reasignment=i.self_task_reasignment,
                               project_business_owner=i.project_business_owner,
                               last_update_date=last_update_fun(), project_objective=i.project_objective
                               )
    form = EDIT_PROJET_FORM(request.POST or None, instance=new_item)

    if form.is_valid():
        form_data = form.save(commit=False)
        form_data.save()
        return redirect(f'/all_task_list_{project_id}')
    context = {
        "form": form,
    }
    return render(request, "edit_project_form_view.html", context)


def project_resouce_select_form(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return render(request, 'project_resource_select_form.html')


def project_resource_individual_form_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    form = PROJECT_RESOURCES_FORM(request.POST or None)
    if form.is_valid():
        form_1 = form.save(commit=False)
        project_id = form.cleaned_data['project_id']
        resource_pool = 'individual'
        resource_role = form.cleaned_data['resource_role']
        individual_resource_id = form.cleaned_data['individual_resource_id']
        resource_id = individual_resource_id.id

        project_resource_table = PROJECT_RESOURCES(project_id_id=project_id.id, resource_id=resource_id,
                                                   resource_pool=resource_pool, resource_role=resource_role,
                                                   created_by=user_login_fun(request),
                                                   last_updated_by=user_login_fun(request),
                                                   creation_date=datetime_functionality(),
                                                   last_update_date=datetime_functionality())
        project_resource_table.save()
        return redirect('/project_individual_resource')
    return render(request, 'project_resource_form_view.html', {'form': form})


def edit_project_resource_individual_form(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    new_item = get_object_or_404(PROJECT_RESOURCES, pk=kwargs['pk'])
    queryset = PROJECT_RESOURCES.objects.select_related().filter(pk=kwargs['pk'])
    for i in queryset:
        data = queryset.update(project_id_id=i.project_id, resource_id=i.individual_resource_id,
                               resource_pool='individual', resource_role=i.resource_role,
                               last_update_date=last_update_fun())
    form = PROJECT_RESOURCES_FORM(request.POST or None, instance=new_item)
    if form.is_valid():
        form_data = form.save(commit=False)
        form_data.save()
        return redirect('/project_individual_resource')
    context = {
        "form": form,
    }
    return render(request, "project_resource_form_view.html", context)


def project_resource_team_form_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    form = PROJECT_RESOURCES_TEAM_FORM(request.POST or None)
    if form.is_valid():
        project_id = form.cleaned_data['project_id']
        resource_pool = 'team'
        team_resource_role = form.cleaned_data['team_resource_role']
        team_resource_id = form.cleaned_data['team_resource_id']
        resource_id = team_resource_id.id
        project_resource_table = PROJECT_RESOURCES(project_id_id=project_id.id, resource_id=resource_id,
                                                   resource_pool=resource_pool, resource_role=team_resource_role,
                                                   created_by=user_login_fun(request),
                                                   last_updated_by=user_login_fun(request),
                                                   creation_date=datetime_functionality(),
                                                   last_update_date=datetime_functionality()
                                                   )
        project_resource_table.save()
        return redirect('/project_team_resource')
    return render(request, 'project_resource_team_form_view.html', {'form': form})


def edit_project_resource_team_form(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    new_item = get_object_or_404(PROJECT_RESOURCES, pk=kwargs['pk'])
    queryset = PROJECT_RESOURCES.objects.select_related().filter(pk=kwargs['pk'])
    for i in queryset:
        resource_pool = 'team'
        data = queryset.update(project_id_id=i.project_id, resource_id=i.resource_id,
                               resource_pool=resource_pool, resource_role=i.resource_role,
                               last_update_date=last_update_fun())
    form = PROJECT_RESOURCES_TEAM_FORM(request.POST or None, instance=new_item)
    if form.is_valid():
        form_data = form.save(commit=False)
        form_data.save()
        return redirect('/project_team_resource')
    context = {
        "form": form,
    }
    return render(request, "project_resource_team_form_view.html", context)


def application_form_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user_id = request.user.id
    user_form = UserForm.objects.filter(user_id=user_id).values('people_id')
    if user_form:
        people_table_check = PEOPLE.objects.filter(id=user_form[0]['people_id']).values('can_create_application')
        if people_table_check[0]['can_create_application'] is True:
            form = APPLICATION_FORM(request.POST or None)
            if form.is_valid():
                form_1 = form.save(commit=False)
                application_description = form.cleaned_data['application_description']
                application_name = form.cleaned_data['application_name']
                application_table = APPLICATION(application_description=application_description,
                                                application_name=application_name,
                                                created_by=user_login_fun(request),
                                                last_updated_by=user_login_fun(request),
                                                creation_date=datetime_functionality(),
                                                last_update_date=datetime_functionality())
                application_table.save()
                return redirect('/application')
            return render(request, 'application_form_view.html', {'form': form})
        else:
            message = 'You do not have sufficient privileges to create the application!'
            return render(request, 'error_page.html', {'message': message})
    else:
        message = 'The User has no people id'
        return render(request, 'error_page.html', {'message': message})
        # return JsonResponse({'Message': 'you do not have enough privileges to create the application!'})


def edit_application_form(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    new_item = get_object_or_404(APPLICATION, pk=kwargs['pk'])
    queryset = APPLICATION.objects.select_related().filter(pk=kwargs['pk'])
    for i in queryset:
        data = queryset.update(application_description=i.application_description, application_id=i.application_id,
                               application_name=i.application_name,
                               last_update_date=last_update_fun()
                               )
    form = APPLICATION_FORM(request.POST or None, instance=new_item)
    if form.is_valid():
        form_data = form.save(commit=False)
        form_data.save()
        return redirect('/application')
    context = {
        "form": form,
    }
    return render(request, "application_form_view.html", context)
