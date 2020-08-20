from .models import PEOPLE,TEAM,PROJECT,PROJECT_RESOURCES,TASK,APPLICATION,NOTIFICATIONS, \
    DOCUMENT,UserForm,APPROVAL_HIERARCHY,TASK_APPROVALS
from .forms import PEOPLE_FORM,TEAM_FORM1,TEAM_FORM2,PROJET_FORM,PROJECT_RESOURCES_FORM, \
    PROJECT_RESOURCES_TEAM_FORM,TASK_FORM,APPLICATION_FORM, \
    DOCUMENT_FORM,TASK_FORM1,SignUpForm
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
from django.contrib.auth.decorators import permission_required,login_required

from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth import get_user_model

User = get_user_model()


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")


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
    email = request.user.email
    print(email,'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    people = PEOPLE.objects.filter(email_id=email).values('id')
    for i in people:
        id_ = i['id']
        print(id_,'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwsssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
        task_approve_details = TASK_APPROVALS.objects.filter(forwarded_to_id=id_, approval_status='awaiting').values('id','task_id', 'forwarded_by')
        print(task_approve_details,'jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
        t_id=[]
        id_=[]
        forward_id=[]
        p_id=[]
        if task_approve_details:
            for i in task_approve_details:
                seq_id = i['id']
                id_.append(seq_id)
                task_id = i['task_id']
                print(task_id,'xxxsssssssssssssssssssssssssssssssssssssssss')
                task_list_val = TASK.objects.filter(id=task_id).values('task_name', 'project_id')
                print(task_list_val,'xxxxxxxxxxxxxxxxxxxxxxxxxxwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
                forwarded_by = i['forwarded_by']
                email_id_ = PEOPLE.objects.filter(id=forwarded_by).values('email_id')
                email = email_id_[0]['email_id']
                # user_id = int(forwarded_by)
                print(email,email_id_,'cccccccccccccccccccccccccccccccccccccccccccccccccccccccc222222222222222222222222222222222222222222222222')
                # # try:
                # user = User.objects.get(id=user_id)
                # print(user, '88888888888888888888888888888888888888888888888888888888888888888888')
                forward_id.append(email)
                print(forward_id, 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx2222222222222222222222222222222222222')
                # except:
                #     messages.error(request, 'No user found!')
                for i in task_list_val:
                    t_id.append(i['task_name'])
                    project_table = PROJECT.objects.filter(id=i['project_id']).values('project_name')
                    p_id.append(project_table[0]['project_name'])
                    print(p_id,t_id,'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
            list_val = zip(t_id,forward_id,p_id,id_)
            print(list_val,'xxxxxxxxxxxmmmmmmmmmmmnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
            context={
                'task_id':task_id,
                'list_val':list_val
            }
            return render(request,'approval_notification.html',context)
        # else:
        #     return render(request, 'approval_notification.html')
        #     message = 'You do not have any notification'
        #     return render(request, 'error_page.html', {'message': message})
    return render(request,'approval_notification.html')


def reject_approval_notification(request,pk):
    # user_details = get_object_or_404(TASK_APPROVALS, pk=pk)
    update_status = TASK_APPROVALS.objects.filter(id=pk).update(approval_status='rejected')
    print(update_status,'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc')
    search_task = TASK_APPROVALS.objects.filter(id=pk).values('task_id')
    print(search_task[0]['task_id'],'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    update_task = TASK.objects.filter(id=search_task[0]['task_id']).update(approval_flag='rejected')
    print(update_task,'11111111111111111111111111111111111111111')
    return redirect('/approvals_list')


def approval_notification_approved(request, pk):
    print(pk,'wwwwwwwwwwwwwwwwwwwwwwwwwwwww')
    update_status = TASK_APPROVALS.objects.filter(id=pk).update(approval_status='approved')
    print(update_status, 'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc')
    search_task = TASK_APPROVALS.objects.filter(id=pk).values('task_id','approval_level','forwarded_to_id')
    print(search_task[0]['task_id'], 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    leval = search_task[0]['approval_level']
    search_project_id = TASK.objects.filter(id=search_task[0]['task_id']).values('project_id_id')
    project_id= search_project_id[0]['project_id_id']
    print(search_project_id, 'cwwwwwwwwwwwwwwsssssssssssssssssssssssssssssssssssssssssssssssss')
    approval_hierachy= APPROVAL_HIERARCHY.objects.filter(project_id_id=project_id,approval_level__gt=leval).values('approval_level','project_id_id','forwarded_to_id').order_by('approval_level')[:1]
    print(approval_hierachy,'666666666666666666666666666666666666666666666666666666666666666666666666')
    if approval_hierachy:
        hierachy_approval_leval= approval_hierachy[0]['approval_level']
        forwarded_to_id= approval_hierachy[0]['forwarded_to_id']
        print(forwarded_to_id,'ccccccccccccccccccccccccccccccccccccccccccccccccccccccc')
        create_task_approval = TASK_APPROVALS(approval_level=hierachy_approval_leval,executed='Yes', approval_status='awaiting',
                                                forwarded_by_id=search_task[0]['forwarded_to_id'],
                                                forwarded_to_id=forwarded_to_id, task_id_id=search_task[0]['task_id'])
        create_task_approval.save()
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    else:
        update_task = TASK.objects.filter(id=search_task[0]['task_id']).update(approval_flag='approved')
        print(update_task, 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
    return redirect('/approvals_list')
    # for level in approval_hierachy:
    #     hierachy_approval_leval = level['approval_level']
    #     hierachy.append(hierachy_approval_leval)
    #     print(hierachy, 'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
    #
    #     forwarded_to_id = level['forwarded_to_id']
    #     print(forwarded_to_id,hierachy_approval_leval,'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    # data_hierachy = str(hierachy).replace("'",'')
    # print(data_hierachy, 'jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
    # import ast
    # json_data = ast.literal_eval(data_hierachy)
    # print(type(json_data), '2222222222333333333333aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    # print(json_data, 'qqqqqqqqqqqaaaaaaaaaaaaaaaaaazzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
    # if 1 in json_data:
    #     no = search_task[0]['approval_level']
    #     print(search_task[0]['approval_level'],'cccccccccc55555555555555555555555555555')
    #     print(all(i >= 1 for i in json_data),'pppppppppppppppppppppppppppppppppppppppppppppppppppppppp')
    #     a =all(i >= 1 for i in json_data)
    #     print(a,'xxxxxxxMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMxxxxxxxxxx')
    #     if a is True:
    #         create_task_approval = TASK_APPROVALS(approval_level=hierachy_approval_leval,
    #                                                   executed='Yes', approval_status='awaiting',
    #                                                   forwarded_by_id=search_task[0]['forwarded_to_id'],
    #                                                   forwarded_to_id=forwarded_to_id, task_id_id=search_task[0]['task_id'])
    #         create_task_approval.save()
    #         print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    #     else:
    #



        # if hierachy_approval_leval <= search_task[0]['approval_level']:
        #     update_task = TASK.objects.filter(id=search_task[0]['task_id']).update(approval_flag='approved')
        #     print(update_task, 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
        # elif hierachy_approval_leval > search_task[0]['approval_level'] and hierachy_approval_leval == search_task[0] :
        #     create_task_approval = TASK_APPROVALS(approval_level=hierachy_approval_leval,
        #                                           executed='Yes', approval_status='awaiting',
        #                                           forwarded_by_id=search_task[0]['forwarded_to_id'],
        #                                           forwarded_to_id=forwarded_to_id, task_id_id=search_task[0]['task_id'])
        #     create_task_approval.save()
        #     print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        # else:
        #     print('trydddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
        # return redirect('/approvals_list')
            # if hierachy_approval_leval == search_task[0]['approval_level']:
        #             # and not(hierachy_approval_leval) > search_task[0]['approval_level']:
        #         # if not( 4 >1):
        #         update_task = TASK.objects.filter(id=search_task[0]['task_id']).update(approval_flag='approved')
        #         print(update_task, 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')

        #     # .objects.filter(id=search_task[0]['task_id']).update(approval_flag='approved')
        #     print(create_task_approval, 'nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
        # else:
        #     update_task = TASK.objects.filter(id=search_task[0]['task_id']).update(approval_flag='approved')
        #     print(update_task, 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')

        #     else:
        #         update_task = TASK.objects.filter(id=search_task[0]['task_id']).update(approval_flag='approved')
        #         print(update_task, '11111111111111111111111111111111111111111')
        # # elif hierachy_approval_leval > search_task[0]['approval_level']
        #         hierachy_approval_leval ==search_task[0]['approval_level']:
        #     update_task = TASK.objects.filter(id=search_task[0]['task_id']).update(approval_flag='approved')
        #     print(update_task, '11111111111111111111111111111111111111111')
        # else:
        #     if hierachy_approval_leval > search_task[0]['approval_level']:
        #         pass
        #     else:
        #         if hierachy_approval_leval == search_task[0]['approval_level']:
        #             update_task = TASK.objects.filter(id=search_task[0]['task_id']).update(approval_flag='approved')
        #             print(update_task, '11111111111111111111111111111111111111111')

            #5>1 than new task approval create
            # if hierachy_approval_leval > search_task[0]['approval_level']:
            #     create_task_approval = TASK_APPROVALS(approval_level=hierachy_approval_leval,
            #                                  executed='Yes',approval_status='awaiting',
            #                                  forwarded_by_id=search_task[0]['forwarded_to_id'],
            #                                  forwarded_to_id= forwarded_to_id,task_id_id=search_task[0]['task_id'])
            #     create_task_approval.save()
            #         # .objects.filter(id=search_task[0]['task_id']).update(approval_flag='approved')
            #     print(create_task_approval, '11111111111111111111111111111111111111111')


    # task_approval = TASK_APPROVALS.objects.all().values('forwarded_to')
    # print(task_approval,'xxxxxxxxxxxxxxxxxxxxxxx')
    # for i in task_approval:
    #     print(i['forwarded_to'],'ccccccccccc33333333333333335555555555555555555')
    #     people = PEOPLE.objects.filter(id=i['forwarded_to']).values('id','email_id')
    #
    #     for p in people:
    #         # try:
    #         print(p['email_id'],'cccccccccccccccccccccsssssssssssssssssssssssssssss')
    #         if p['email_id'] == email:
    #             p_id = p['id']
    #             task_approve_details =TASK_APPROVALS.objects.filter(forwarded_to=p_id).values('task_id','forwarded_by')
    #             t_id=[]
    #             forward_id=[]
    #             p_id=[]
    #             for i in task_approve_details:
    #                 task_id = i['task_id']
    #                 task_list_val = TASK.objects.filter(id=task_id).values('task_name', 'project_id')
    #                 forwarded_by = i['forwarded_by']
    #                 user_id = int(forwarded_by)
    #                 user = User.objects.get(id=user_id)
    #                 forward_id.append(user.email)
    #                 for i in task_list_val:
    #                     t_id.append(i['task_name'])
    #                     project_table = PROJECT.objects.filter(id=i['project_id']).values('project_name')
    #                     p_id.append(project_table[0]['project_name'])
    #             list_val = zip(t_id,forward_id,p_id)
    #             context={
    #                 'list_val':list_val
    #             }
    #             return render(request,'approval_notification.html',context)
    #         else:
    #             message = 'You do not have any notification'
    #             return render(request, 'error_page.html', {'message': message})
            # except:
            #     pass


def error(request):
    return render(request,'error_page.html')

@login_required
def index(request):
    return render(request, 'base1.html')


def all_projects_list(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user_id=request.user.id
    p_id = UserForm.objects.filter(user_id=user_id).values_list('people_id')
    if p_id:
        for i in p_id:
            team_check_p_id = TEAM.objects.all().values('all_members','id')
            t_id = []
            for d in team_check_p_id:
                p_id_ = d['all_members']
                id = d['id']
                try:
                    if f'{i[0]}' in p_id_:
                        t_id.append(id)
                except:
                    pass
            team_id =str(t_id).replace('[','(').replace(']',')')
            # team_id =()
            project_resource = PROJECT_RESOURCES.objects.filter(Q(resource_id=i[0]) | Q(resource_id__in= team_id)).values('project_id_id')
            project_list = PROJECT.objects.all().filter(id__in=project_resource).order_by('-id')
            return render(request, 'project_list_view.html', {'project_list': project_list})
    else:
        print('try again ================')
    # project_list = PROJECT.objects.all().filter(login_create_user_id=user_id).order_by('-id')
    # project_list = PROJECT.objects.all().all().order_by('-id')
    # return render(request,'project_list_view.html',{'project_list':project_list})


def show_owner(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    project = PROJECT.objects.filter(id =pk).values('project_name')
    owner_details = PROJECT_RESOURCES.objects.all().filter(project_id=pk,resource_role='owner').values('resource_id')
    first_name = []
    last_name = []
    # if owner_details:
    for j in owner_details:
        resource_id = j['resource_id']
        people_list_ = PEOPLE.objects.filter(id=resource_id).values('p_first_name', 'p_last_name')
        for p in people_list_:
            f_name =p['p_first_name']
            l_name =p['p_last_name']
            first_name.append(f_name)
            last_name.append(l_name)
    # else:
    #     return JsonResponse({'Message':f'{project} has no owner'})
    people_lists= zip(first_name, last_name)
    context = {
        'project': project,
        'people_lists': people_lists
    }
    return render(request, 'project_owner_details.html', context)


def parent_task_form_view(request,pk):
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


def task_details_view(request,pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    document = DOCUMENT.objects.filter(task_id = pk)
    task = TASK.objects.filter(id=pk)
    #     .values_list('task_name','description',
    # 'task_by_id','assigned_by_id','assigned_to_id','status','reassignable','start_date','end_date',
    # 'expected_end_date','task_type','last_update_date','parent_task','approval_flag','project_id')
    # for i in task:
    #     print(i,'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc')
    #     task_name = i[0],
    #     description = i[0],
    #     status = i[5],
    #     reassignable = i[6],
    #     start_date = i[7],
    #     end_date = i[8],
    #     expected_end_date = i[9],
    #     task_type = i[10],
    #     last_update_date = i[11],
    #     parent_task = i[12],
    #     approval_flag = i[13],
    #     project_id = i[14],
    #     assign_to_ = i[4],
    #     assign_by_ = i[3],
    #     task_by_ = i[2]
    #     print(task_by_,'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    #     assign_to_id = str(assign_to_).replace("(",'').replace(",)",'')
    #     assign_by_id = str(assign_by_).replace("(",'').replace(",)",'')
    #     task_by_id = str(task_by_).replace("(",'').replace(",)",'')
    #     assign_to = PEOPLE.objects.filter(id = assign_to_id).values('p_first_name', 'p_last_name')
    #     assign_by = PEOPLE.objects.filter(id = assign_by_id).values('p_first_name', 'p_last_name')
    #     task_by = PEOPLE.objects.filter(id = task_by_id).values('p_first_name', 'p_last_name')
    #     task_list = zip(task_name,description,status,reassignable,start_date ,end_date ,
    #                     expected_end_date ,task_type ,last_update_date,parent_task,approval_flag,project_id)
    #     context = {
    #         "task": task_list,
    #         "document": document,
    #         "assign_to": assign_to,
    #         "assign_by": assign_by,
    #         "task_by": task_by
    #
    #     }
    #     return render(request, 'task_details_form_view.html', context)


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
        assign_to_id = str(assign_to_).replace("(",'').replace(",)",'')
        assign_by_id = str(assign_by_).replace("(",'').replace(",)",'')
        task_by_id = str(task_by_).replace("(",'').replace(",)",'')
        assign_to = PEOPLE.objects.filter(id = assign_to_id).values('p_first_name', 'p_last_name')
        assign_by = PEOPLE.objects.filter(id = assign_by_id).values('p_first_name', 'p_last_name')
        task_by = PEOPLE.objects.filter(id = task_by_id).values('p_first_name', 'p_last_name')
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
    return render(request,'people_list_view.html',{'people_list':people_list})


def all_application_list(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    application_list = APPLICATION.objects.all().order_by('-id')
    return render(request,'application_list_view.html',{'application_list':application_list})


def project_all_task_list(request,pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    project_resrc = PROJECT_RESOURCES.objects.filter(project_id=pk).values('resource_id','resource_role')
    first_name=[]
    last_name=[]
    email=[]
    contact=[]
    resource_role_=[]
    for i in project_resrc:
        resource_role = i['resource_role']
        resource_id = i['resource_id']
        people_list_ = PEOPLE.objects.filter(id=resource_id).values('p_first_name', 'p_last_name','email_id','contact_no')
        resource_role_.append(resource_role)
        for p in people_list_:
            f_name =p['p_first_name']
            l_name =p['p_last_name']
            email_id =p['email_id']
            contact_no =p['contact_no']
            first_name.append(f_name)
            last_name.append(l_name)
            contact.append(contact_no)
            email.append(email_id)
    people_list = zip(first_name,last_name,email,contact,resource_role_)
    # people_list =TASK.objects.filter(project_id=pk).values('assigned_to_id')
    # people_list =PEOPLE.objects.filter(id__in=task_db)
    # task_list = TASK.objects.all().filter(project_id=pk).order_by('-id')
    project_list = PROJECT.objects.all().filter(id=pk).order_by('-id')
    last_activity_Date = TASK.objects.all().filter(project_id=pk).values('last_update_date').order_by('-last_update_date')[:1]
    task_list = TASK.objects.all().filter(project_id=pk).values('id','task_name',
    'task_by_id','assigned_by_id','assigned_to_id','status','reassignable','start_date','end_date',
    'expected_end_date','task_type').order_by('-id')
    id_=[]
    task_name =[]
    task_by_f_name=[]
    task_by_l_name=[]
    assign_by_f_name=[]
    assign_by_l_name=[]
    assign_to_l_name=[]
    assign_to_f_name=[]
    status =[]
    start_date =[]
    reassignable =[]
    end_date =[]
    expected_end_date =[]
    task_type =[]

    for i in task_list:
        id = i['id']
        t_name = i['task_name']
        status_ = i['status']
        s_date = i['start_date']
        e_date = i['end_date']
        e_e_date = i['expected_end_date']
        t_type = i['task_type']
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
        expected_end_date.append(e_e_date)
        reassignable.append(re_assignable)
        end_date.append(e_date)
        start_date.append(s_date)
        status.append(status_)
    task_list_ = zip(id_, task_name,status,start_date,end_date,expected_end_date,task_type,reassignable,
                     task_by_f_name,task_by_l_name,assign_by_f_name,assign_by_l_name,assign_to_f_name,
                     assign_to_l_name)
    context = {'task_list': task_list_,
               'project_list': project_list,
               'people_list': people_list,
               # 'assign_to': assign_to,
               'pk': pk,
               # 'id_':str(id),
               # 'task_people': task_people,
               'last_activity_Date': last_activity_Date,
               # 'task_by': task_by
               }
    return render(request, 'project_all_task_view.html', context)


def task_form_view_from_all_task(request,pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    project_model = PROJECT.objects.filter(id=pk).values_list('task_creation','project_name')
    project_name = project_model[0][1]
    if project_model[0][0] =='self':
        form = TASK_FORM1(request.POST or None)
        if form.is_valid():
            form_1 = form.save(commit=False)
            project_id = pk
            request.session['project_id'] = project_id
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
                approval_flag='on_going'
            try:
                parent_task = parent_task.id
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
            try:
                task_by = task_by.id
            except:
                task_by = None
            if start_date >end_date or start_date >expected_end_date:
                messages.error(request, 'Expected/End date must be equal or greater than to start date')
            elif end_date < expected_end_date:
                messages.error(request, 'Expected End date must be equal or less than to end date ')
            else:
                task_table_save = TASK(project_id_id=pk, task_name=task_name, task_by_id=task_by,
                                       assigned_by_id=assigned_by, assigned_to_id=assigned_to,
                                       start_date=start_date, end_date=end_date, description=description,
                                       status=status, reassignable=reassignable, parent_task_id=parent_task,
                                       created_by=user_login_fun(request), last_updated_by=user_login_fun(request),
                                       creation_date=datetime_functionality(), expected_end_date=expected_end_date,
                                       last_update_date=datetime_functionality(),task_type=task_type,
                                       approval_flag=approval_flag)
                task_table_save.save()
                table_task = task_table_save.id
                id_ = ''.join(c for c in str(table_task) if c.isdigit())
                request.session['id_'] = id_
                data = TASK.objects.filter(id=id_).values('approval_flag','project_id_id')
                # Approval Logiv
                print(data[0]['project_id_id'],'22222222222222222222222222222222222222222222222')
                if data[0]['approval_flag'] == 'on_going':
                    approval_hierarchy = APPROVAL_HIERARCHY.objects.filter(project_id_id=data[0]['project_id_id'],
                                                        approval_level='1').values('approval_level','forwarded_to')
                    if approval_hierarchy:
                        forwarded_to = approval_hierarchy[0]['forwarded_to']
                        print(forwarded_to,'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc')
                        approval_level = approval_hierarchy[0]['approval_level']
                        user_id_ = request.user.id
                        print(user_id_,'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                        userform = UserForm.objects.filter(user_id=user_id_).values('people_id')
                        if userform:
                            print(userform,'ccccccccccccccccccccccccccccccccccccccc')

                            p_id=userform[0]['people_id']
                            print(p_id,'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                            cursor =connection.cursor()
                            approval_task = f'''
                            INSERT INTO public.app_task_approvals(
                                approval_level, executed, approval_status, forwarded_by_id, forwarded_to_id, task_id_id)
                                VALUES ('{approval_level}', 'Yes','awaiting',{p_id} , {forwarded_to}, {id_});
                            '''
                            cursor.execute(approval_task)
                        else:
                            print('Try again!')
                return redirect(f"/document_{pk}")
        else:
            print(form.errors,'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
        return render(request, 'task_form_view_from_all_task_list.html', {'form': form, 'project_name': project_name})
    else:
        if project_model[0][0] == 'owner':
            user_id = request.user.id
            user_form = UserForm.objects.filter(user_id = user_id).values('people_id')
            if user_form:
                project_resrc = PROJECT_RESOURCES.objects.filter(project_id=pk, resource_role='owner').values('resource_id')
                if project_resrc:
                    if project_resrc[0]['resource_id'] ==user_form[0]['people_id']:
                        form = TASK_FORM1(request.POST or None)
                        if form.is_valid():
                            form_1 = form.save(commit=False)
                            project_id = pk
                            request.session['project_id'] = project_id
                            task_by = form.cleaned_data['task_by']
                            task_name = form.cleaned_data['task_name']
                            description = form.cleaned_data['description']
                            assigned_by = form.cleaned_data['assigned_by']
                            assigned_to = form.cleaned_data['assigned_to']
                            start_date = form.cleaned_data['start_date']
                            end_date = form.cleaned_data['end_date']
                            expected_end_date = form.cleaned_data['expected_end_date']
                            status = form.cleaned_data['status']
                            reassignable = form.cleaned_data['reassignable']
                            parent_task = form.cleaned_data['parent_task']
                            task_type = form.cleaned_data['task_type']
                            if task_type == 'support':
                                approval_flag = 'na'
                            else:
                                approval_flag = 'on_going'
                            try:
                                parent_task = parent_task.id
                            except:
                                parent_task = None
                            task_table_save = TASK(project_id_id=project_id, task_name=task_name, task_by_id=task_by.id,
                                                   assigned_by_id=assigned_by.id, assigned_to_id=assigned_to.id,
                                                   start_date=start_date, end_date=end_date, description=description,
                                                   status=status, reassignable=reassignable, parent_task_id=parent_task,
                                                   created_by=user_login_fun(request), last_updated_by=user_login_fun(request),
                                                   creation_date=datetime_functionality(), expected_end_date=expected_end_date,
                                                   last_update_date=datetime_functionality(),task_type=task_type,
                                                   approval_flag=approval_flag
                                                   )
                            task_table_save.save()
                            table_task = task_table_save.id
                            id_ = ''.join(c for c in str(table_task) if c.isdigit())
                            request.session['id_'] = id_
                            data = TASK.objects.filter(id=id_).values('approval_flag', 'project_id_id')
                            print(data, 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
                            if data[0]['approval_flag'] == 'on_going':
                                print('xxxxxxxxxxxxxxxxxxxxxxxxx')
                                approval_hierarchy = APPROVAL_HIERARCHY.objects.filter(
                                    project_id_id=data[0]['project_id_id'],
                                    approval_level='1').values('approval_level', 'forwarded_to')
                                if approval_hierarchy:
                                    forwarded_to = approval_hierarchy[0]['forwarded_to']
                                    approval_level = approval_hierarchy[0]['approval_level']

                                    print(approval_hierarchy, 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                                    user_id_ = request.user.id
                                    userform = UserForm.objects.filter(user_id=user_id_).values('people_id')
                                    if userform:
                                        print(userform, 'ccccccccccccccccccccccccccccccccccccccc')

                                        p_id = userform[0]['people_id']
                                        print(p_id, 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                                        cursor = connection.cursor()
                                        approval_task = f'''
                                                              INSERT INTO public.app_task_approvals(
                                                                  approval_level, executed, approval_status, forwarded_by_id, forwarded_to_id, task_id_id)
                                                                  VALUES ('{approval_level}', 'Yes','awaiting',{p_id} , {forwarded_to}, {id_});
                                                              '''
                                        cursor.execute(approval_task)
                                    else:
                                        print('Try again!')

                            return redirect(f"/document_{pk}")
                        return render(request, 'task_form_view_from_all_task_list.html',{'form': form, 'project_name': project_name})
                    else:
                        message = 'You do not have sufficient privileges to create this task!'
                        return render(request, 'error_page.html', {'message': message})
                else:
                    message = 'You do not have sufficient privileges to create this task!'
                    return render(request, 'error_page.html', {'message': message})
            else:
                message = 'You do not have sufficient privileges to create this task!'
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
                document_location = form.cleaned_data['document_location']
                create_doc = DOCUMENT(document_name=document_name, document_location=document_location,
                                      task_id=id_, project_id=project_id,creation_date=datetime_functionality(),
                                      last_update_date=datetime_functionality(),created_by=user_login_fun(request),
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
        'form':form,
        'photos_list':photos_list,
        'id':id_,
        'pk':pk,
        'project_id':project_id
    }
    return render(request, 'doc_form_view_from_all_task.html',context)


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
    return render(request, 'project_resource_from_all_task.html', {'form': form,'project':project,'pk':pk})


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
    return render(request, 'project_resource_team_from_all_task.html', {'form': form,'project':project,'pk':pk})
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
    current_date = now.strftime("%d-%m-%Y_%I-%M-%S_%p")
    return current_date


def last_update_fun():
    now = datetime.now()
    update_date = now.strftime("%d-%m-%Y_%I-%M-%S_%p")
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
        self.form_1 = self.form_class(prefix='form_1')
        return super(PEOPLE_FORM_VIEW, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        self.form_1 = self.form_class(prefix='form_1', data=request.POST)
        if self.form_1.is_valid():
            form_db = self.form_1.save(commit=False)
            p_first_name = self.form_1.cleaned_data['p_first_name']
            p_last_name = self.form_1.cleaned_data['p_last_name']
            email_id = self.form_1.cleaned_data['email_id']
            contact_no = self.form_1.cleaned_data['contact_no']
            department = self.form_1.cleaned_data['department']
            can_create_project = self.form_1.cleaned_data['can_create_project']
            can_create_application = self.form_1.cleaned_data['can_create_application']
            people_table = PEOPLE(p_first_name=p_first_name,p_last_name=p_last_name,
                                  can_create_application=can_create_application,can_create_project=can_create_project,
                                  email_id=email_id,contact_no=contact_no,created_by=user_login_fun(request),
                                  department=department,last_updated_by=user_login_fun(request),
                                  creation_date=datetime_functionality(),last_update_date=datetime_functionality())
            people_table.save()
            return redirect(f'/signup_{people_table.id}')
        else:
            return HttpResponse(self.form_1.errors)

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


def signup(request,pk):
    user_detail = PEOPLE.objects.filter(id=pk).values_list('p_first_name', 'p_last_name', 'email_id')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.is_staff=True
            first_name = user_detail[0][0]
            last_name =user_detail[0][1]
            email = user_detail[0][2]
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.save()
            cursor =connection.cursor()
            user_form_create =f'''
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
    new_item = get_object_or_404(PEOPLE,  pk=kwargs['pk'])
    queryset = PEOPLE.objects.select_related().filter(pk=kwargs['pk'])
    for i in queryset:
        data = queryset.update(p_first_name=i.p_first_name,p_last_name=i.p_last_name,
                               email_id=i.email_id,contact_no=i.contact_no,
                               department=i.department,last_update_date=last_update_fun())
    form = PEOPLE_FORM(request.POST or None, instance=new_item)
    if form.is_valid():
        form_data = form.save(commit=False)
        form_data.save()
        return redirect('/people')
    context = {
        "form": form,
    }
    return render(request, "update_people_form_view.html", context)


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
                id =i[0]
                all_member=[f'{i[15]}']
                memberid= [f'{team_member_id.id}']
                all_member.extend(memberid)
                update_members = str(all_member).replace("'",'').replace('[','').replace(']','')
                final_query_ = list(update_members.split(','))
                final_query = [x.strip(' ') for x in final_query_]
                for i in final_query:
                    if final_query.count(i) > 1:
                        final_query.remove(i)
                final_queries = [i for i in final_query if i != '0']

                update_members_team = str(final_queries).replace("'","").replace('[','').replace(']','')
                update_row_member = f'''
                                UPDATE public.app_team
                 SET all_members = '{update_members_team}' , last_update_date='{last_update_fun()}'
                                    WHERE id = '{id}';
                                                '''
                cursor.execute(update_row_member)
            return redirect('/team_add')
        elif not queryset:
            team_table_save = TEAM(team_name=team_name,team_description=team_description,
                                   all_members=team_member_id.id, created_by=user_login_fun(request),
                                   last_updated_by=user_login_fun(request),creation_date=datetime_functionality(),
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
        model_data=[]
    context = {
        "form": form,
        'model_data':model_data,
        'team_name':team_name,
        'team_description':team_description,
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
        task_table_save = TASK(project_id_id=project_id.id,task_name=task_name, task_by_id=task_by.id,
                               assigned_by_id=assigned_by.id, assigned_to_id=assigned_to.id,
                               start_date=start_date, end_date=end_date,description=description,
                               status=status, reassignable=reassignable, parent_task_id=parent_task,
                               created_by=user_login_fun(request), last_updated_by=user_login_fun(request),
                               creation_date=datetime_functionality(),expected_end_date=expected_end_date,
                               last_update_date=datetime_functionality(),task_type=task_type,
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
                                      task_id=id_, project_id=project_id,creation_date=datetime_functionality(),
                                      last_update_date=datetime_functionality(),created_by=user_login_fun(request),
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
        'form':form,
        'photos_list':photos_list,
        'id':id_,
        'project_id':project_id
    }
    return render(request, 'doc_form_view.html',context)


def edit_task_form(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    new_item = get_object_or_404(TASK,  pk=kwargs['pk'])
    queryset = TASK.objects.select_related().filter(pk=kwargs['pk'])
    for i in queryset:
        data = queryset.update(project_id=i.project_id,task_by_id=i.task_by,task_type=i.task_type,
                               assigned_by_id=i.assigned_by,assigned_to_id=i.assigned_to,
                               start_date=i.start_date,end_date=i.end_date,expected_end_date=i.expected_end_date,
                               status=i.status,reassignable=i.reassignable,parent_task_id=i.parent_task,
                               last_update_date=last_update_fun())
    form = TASK_FORM(request.POST or None, instance=new_item)
    if form.is_valid():
        form_data = form.save(commit=False)
        form_data.save()
        return redirect('/task')

    context = {
        "form": form,
        # "document":document
    }
    return render(request, "task_form_view.html", context)


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
                    self_task_reasignment = form.cleaned_data['self_task_reasignment']
                    if start_date > expected_end_date:
                        messages.error(request, 'Expected End date must be equal or greater than to start date')
                    else:
                        project_table_save = PROJECT(project_name=project_name,application_id_id=application_id,
                                                     project_description=project_description, project_type=project_type,start_date=start_date,expected_end_date=expected_end_date,
                                                     status=status,task_creation=task_creation,login_create_user=user_id,
                                                     self_task_reasignment=self_task_reasignment,
                                                     created_by=user_login_fun(request), last_updated_by=user_login_fun(request),
                                                     creation_date=datetime_functionality(),
                                                     last_update_date=datetime_functionality()
                                                     )
                        project_table_save.save()
                        table_task = project_table_save.id
                        id_ = ''.join(c for c in str(table_task) if c.isdigit())
                        print(id_,'cccccccccccccccccccccccccc333333333333333333333333333333333333')
                        # try:
                        user = request.user.id
                        print(user,'c2222222222222222222222222222222222222222222222222222')
                        people_id = UserForm.objects.filter(user_id=user).values('people_id')[:1]
                        print(people_id,'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
                        p_id = people_id[0]['people_id']
                        project_resource = PROJECT_RESOURCES(project_id_id=id_, resource_pool='individual',
                                                             resource_role='creater', resource_id=p_id,
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
    new_item = get_object_or_404(PROJECT,  pk=kwargs['pk'])
    queryset = PROJECT.objects.select_related().filter(pk=kwargs['pk'])
    for i in queryset:
        data = queryset.update(project_name=i.project_name,application_id=i.application_id,
                               project_type=i.project_type,expected_end_date=i.expected_end_date,
                               end_date=i.end_date,project_description=i.project_description,
                               status=i.status,task_creation=i.task_creation,
                               self_task_reasignment=i.self_task_reasignment,
                               last_update_date=last_update_fun()
                               )
    form = PROJET_FORM(request.POST or None, instance=new_item)

    if form.is_valid():
        form_data = form.save(commit=False)
        form_data.save()
        return redirect('/all_projects_list')
    context = {
        "form": form,
    }
    return render(request, "project_form_view.html", context)

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

        project_resource_table = PROJECT_RESOURCES(project_id_id=project_id.id,resource_id=resource_id,
                                                   resource_pool=resource_pool,resource_role=resource_role,
                                                   created_by=user_login_fun(request), last_updated_by=user_login_fun(request),
                                                   creation_date=datetime_functionality(),
                                                   last_update_date=datetime_functionality())
        project_resource_table.save()
        return redirect('/project_individual_resource')
    return render(request, 'project_resource_form_view.html', {'form': form})


def edit_project_resource_individual_form(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    new_item = get_object_or_404(PROJECT_RESOURCES,  pk=kwargs['pk'])
    queryset = PROJECT_RESOURCES.objects.select_related().filter(pk=kwargs['pk'])
    for i in queryset:
        data = queryset.update(project_id_id=i.project_id,resource_id=i.individual_resource_id,
                               resource_pool='individual',resource_role=i.resource_role,
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
        project_resource_table = PROJECT_RESOURCES(project_id_id=project_id.id,resource_id=resource_id,
                                                   resource_pool=resource_pool,resource_role=team_resource_role,
                                                   created_by=user_login_fun(request), last_updated_by=user_login_fun(request),
                                                   creation_date=datetime_functionality(),
                                                   last_update_date=datetime_functionality()
                                                   )
        project_resource_table.save()
        return redirect('/project_team_resource')
    return render(request, 'project_resource_team_form_view.html', {'form': form})


def edit_project_resource_team_form(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    new_item = get_object_or_404(PROJECT_RESOURCES,  pk=kwargs['pk'])
    queryset = PROJECT_RESOURCES.objects.select_related().filter(pk=kwargs['pk'])
    for i in queryset:
        resource_pool='team'
        data = queryset.update(project_id_id=i.project_id,resource_id=i.resource_id,
                               resource_pool=resource_pool,resource_role=i.resource_role,
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
                                                created_by=user_login_fun(request), last_updated_by=user_login_fun(request),
                                                creation_date=datetime_functionality(),
                                                last_update_date=datetime_functionality())
                application_table.save()
                return redirect('/application')
            return render(request, 'application_form_view.html', {'form': form})
        else:
            message='You do not have sufficient privileges to create the application!'
            return render(request,'error_page.html',{'message':message})
    else:
        message = 'The User has no people id'
        return render(request, 'error_page.html', {'message': message})
            # return JsonResponse({'Message': 'you do not have enough privileges to create the application!'})


def edit_application_form(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    new_item = get_object_or_404(APPLICATION,  pk=kwargs['pk'])
    queryset = APPLICATION.objects.select_related().filter(pk=kwargs['pk'])
    for i in queryset:
        data = queryset.update(application_description=i.application_description,application_id=i.application_id,
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

