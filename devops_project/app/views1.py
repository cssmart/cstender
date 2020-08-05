from django.shortcuts import render
from .models import PEOPLE,TEAM,PROJECTS,PROJECT_RESOURCES,TASK,APPLICATION,NOTIFICATIONS
from .forms import PEOPLE_FORM,TEAM_FORM1,TEAM_FORM2,PROJET_FORM,PROJECT_RESOURCES_FORM,\
    PROJECT_RESOURCES_TEAM_FORM,CronForm,TASK_FORM,APPLICATION_FORM
from django.views.generic import TemplateView
from django.shortcuts import redirect, render_to_response, get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from datetime import datetime


def datetime_functionality():
    now = datetime.now()
    current_date = now.strftime("%d-%m-%Y_%I-%M-%S_%p")
    return current_date

def last_update_fun():
    now = datetime.now()
    update_date = now.strftime("%d-%m-%Y_%I-%M-%S_%p")
    return update_date

def day_view(request):
    form = CronForm(request.POST or None)
    if form.is_valid():
        form1 = form.save(commit=False)
        return redirect('/team_form')
    return render(request, 'test.html', {'form': form})


class PEOPLE_FORM_VIEW(TemplateView):
    '''
    people form view
    '''
    form_class = PEOPLE_FORM
    form_1 = None

    def get(self, request, *args, **kwargs):
        self.form_1 = self.form_class(prefix='form_1')
        return super(PEOPLE_FORM_VIEW, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.form_1 = self.form_class(prefix='form_1', data=request.POST)
        if self.form_1.is_valid() or request.user.is_authenticated:
            user_id = request.user
            form_db = self.form_1.save(commit=False)
            p_first_name = self.form_1.cleaned_data['p_first_name']
            p_last_name = self.form_1.cleaned_data['p_last_name']
            email_id = self.form_1.cleaned_data['email_id']
            contact_no = self.form_1.cleaned_data['contact_no']
            department = self.form_1.cleaned_data['department']
            people_table = PEOPLE(p_first_name=p_first_name,p_last_name=p_last_name,
                                  email_id=email_id,contact_no=contact_no,created_by=user_id,
                                  department=department,last_updated_by=user_id,
                                  creation_date=datetime_functionality(),last_update_date=datetime_functionality())
            people_table.save()
            return redirect('/people')
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


def edit_people_form(request, **kwargs):
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
    form = TEAM_FORM1(request.POST or None)
    if form.is_valid():
        form_1 = form.save(commit=False)
        team_name = form.cleaned_data['team_name']
        team_description = form.cleaned_data['team_description']
        request.session['team_name'] = team_name
        request.session['team_description'] = team_description
        return redirect('/team_form')
    return render(request, 'team_view_form1.html', {'form': form})


def team_view_2(request):
    form = TEAM_FORM2(request.POST or None)
    if form.is_valid() or request.user.is_authenticated:
        user_id = request.user
        print(user_id,'wpwwwwwwwwwwwwwwwwwwwwwwwww')
        form_1 = form.save(commit=False)
        team_name = request.session.get('team_name')
        team_description = request.session.get('team_description')
        print(team_name, team_description,'ppppppppppppppppppppppppp')
        team_member_id = form.cleaned_data['team_member']
        print(team_member_id,'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        team_table_save = TEAM(team_name=team_name,team_description=team_description,
                               team_member_id=team_member_id.id, created_by=user_id,
                               last_updated_by=user_id,creation_date=datetime_functionality(),
                               last_update_date=datetime_functionality())
        team_table_save.save()
        return redirect('/team_form')
    model_data = TEAM.objects.all()
    return render(request, 'team_form_view.html', {'form': form,'model_data':model_data})


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
    form = TASK_FORM(request.POST or None)
    if form.is_valid() or request.user.is_authenticated:
        user_id = request.user
        form_1 = form.save(commit=False)
        project_id = form.cleaned_data['project_id']
        task_by = form.cleaned_data['task_by']
        assigned_by = form.cleaned_data['assigned_by']
        assigned_to = form.cleaned_data['assigned_to']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        status = form.cleaned_data['status']
        reassignable = form.cleaned_data['reassignable']
        parent_task = form.cleaned_data['parent_task']
        print(project_id,'oooooooooooooooooo')
        task_table_save = TASK(project_id=project_id.id,task_by_id=task_by.id,
                               assigned_by_id=assigned_by.id,assigned_to_id=assigned_to.id,
                               start_date=start_date,end_date=end_date,
                               status=status,reassignable=reassignable,parent_task=parent_task,
                               created_by=user_id, last_updated_by=user_id,
                               creation_date=datetime_functionality(),
                               last_update_date=datetime_functionality()
                               )
        task_table_save.save()
        return redirect('/task')
    return render(request, 'task_form_view.html', {'form': form})


def edit_task_form(request, **kwargs):
    new_item = get_object_or_404(PEOPLE,  pk=kwargs['pk'])
    queryset = TASK.objects.select_related().filter(pk=kwargs['pk'])
    for i in queryset:
        data = queryset.update(project_id=i.project_id.id,task_by_id=i.task_by.id,
                               assigned_by_id=i.assigned_by.id,assigned_to_id=i.assigned_to.id,
                               start_date=i.start_date,end_date=i.end_date,
                               status=i.status,reassignable=i.reassignable,parent_task=i.parent_task,
                               last_update_date=last_update_fun())
    form = TASK_FORM(request.POST or None, instance=new_item)
    if form.is_valid():
        form_data = form.save(commit=False)
        form_data.save()
        return redirect('/task')
    context = {
        "form": form,
    }
    return render(request, "task_form_view.html", context)


def project_form_view(request):
    form = PROJET_FORM(request.POST or None)
    if form.is_valid() or request.user.is_authenticated:
        user_id = request.user
        form_1 = form.save(commit=False)
        project_name = form.cleaned_data['project_name']
        application_id = form.cleaned_data['application_id']
        project_type = form.cleaned_data['project_type']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        status = form.cleaned_data['status']
        task_creation = form.cleaned_data['task_creation']
        self_task_reasignment = form.cleaned_data['self_task_reasignment']
        project_table_save = PROJECTS(project_name=project_name,application_id=application_id.id,
                                      project_type=project_type,start_date=start_date,end_date=end_date,
                                      status=status,task_creation=task_creation,
                                      self_task_reasignment=self_task_reasignment,
                                      created_by=user_id, last_updated_by=user_id,
                                      creation_date=datetime_functionality(),
                                      last_update_date=datetime_functionality()
                                      )
        project_table_save.save()
        return redirect('/project')
    return render(request, 'project_form_view.html', {'form': form})


def project_resouce_select_form(request):
    return render(request, 'project_resource_select_form.html')


def project_resource_individual_form_view(request):
    form = PROJECT_RESOURCES_FORM(request.POST or None)
    if form.is_valid() or request.user.is_authenticated:
        user_id = request.user
        form_1 = form.save(commit=False)
        project_id = form.cleaned_data['project_id']
        resource_pool = 'individual'
        resource_role = form.cleaned_data['resource_role']
        individual_resource_id = form.cleaned_data['individual_resource_id']
        resource_id = individual_resource_id.id

        project_resource_table = PROJECT_RESOURCES(project_id_id=project_id.id,resource_id=resource_id,
                                                   resource_pool=resource_pool,resource_role=resource_role,
                                                   created_by=user_id, last_updated_by=user_id,
                                                   creation_date=datetime_functionality(),
                                                   last_update_date=datetime_functionality())
        project_resource_table.save()
        return redirect('/project_individual_resource')
    return render(request, 'project_resource_form_view.html', {'form': form})


def project_resource_team_form_view(request):
    form = PROJECT_RESOURCES_TEAM_FORM(request.POST or None)
    if form.is_valid() or request.user.is_authenticated:
        user_id = request.user
        project_id = form.cleaned_data['project_id']
        resource_pool = 'team'
        resource_role = form.cleaned_data['resource_role']
        team_resource_id = form.cleaned_data['team_resource_id']
        resource_id = team_resource_id.id
        project_resource_table = PROJECT_RESOURCES(project_id_id=project_id.id,resource_id=resource_id,
                                                   resource_pool=resource_pool,resource_role=resource_role,
                                                   created_by=user_id, last_updated_by=user_id,
                                                   creation_date=datetime_functionality(),
                                                   last_update_date=datetime_functionality()
                                                   )
        project_resource_table.save()
        return redirect('/project_team_resource')
    return render(request, 'project_resource_team_form_view.html', {'form': form})


def application_form_view(request):
    form = APPLICATION_FORM(request.POST or None)
    if form.is_valid() or request.user.is_authenticated:
        user_id = request.user
        form_1 = form.save(commit=False)
        application_description = form.cleaned_data['application_description']
        application_id = form.cleaned_data['application_id']
        application_name = form.cleaned_data['application_name']
        application_table = APPLICATION(application_description=application_description,application_id=application_id,
                                        application_name=application_name,
                                        created_by=user_id, last_updated_by=user_id,
                                        creation_date=datetime_functionality(),
                                        last_update_date=datetime_functionality())
        application_table.save()
        return redirect('/application')
    return render(request, 'application_form_view.html', {'form': form})

