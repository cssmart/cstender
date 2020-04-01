from django.shortcuts import render
from django.shortcuts import redirect, render_to_response, get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from .forms import VisitorManagementFormCreate
from django.views.generic import TemplateView
from django.conf import settings
from .models import VisitorManagementForm
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
import smtplib
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
import requests
import datetime

class VisitorFormView(TemplateView):
    form_class = VisitorManagementFormCreate
    form_1 = None

    def get(self, request, *args, **kwargs):
        self.form_1 = self.form_class(prefix='form_1')
        return super(VisitorFormView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.form_1 = self.form_class(prefix='form_1', data=request.POST)
        if self.form_1.is_valid():
            try:
                form_db = self.form_1.save(commit=False)
                x = datetime.datetime.now()
                date = x.strftime("%Y-%m-%d %H:%M:%S")
                print(date)
                name =self.form_1.cleaned_data['name']
                self.request.session['name'] = name
                contact_number = self.form_1.cleaned_data['contact_number']
                self.request.session['contact_number'] = contact_number
                company = self.form_1.cleaned_data['company']
                self.request.session['company'] = company
                person_to_meet = self.form_1.cleaned_data['person_to_meet']
                self.request.session['person_to_meet'] = person_to_meet
                reason =  self.form_1.cleaned_data['reason']
                self.request.session['reason'] = reason
                p = VisitorManagementForm(name=name, contact_number=contact_number, company=company,
                                          person_to_meet=person_to_meet, reason=reason,v_date_time=date)
                p.save()
                url_create_yes = f'http://127.0.0.1:8000/vms/{p.id}/y'
                url_create_no = f'http://127.0.0.1:8000/vms/{p.id}/n'
                ctx = {
                    'url_create_yes':url_create_yes,
                    'url_create_no':url_create_no,
                    'visit_id':p.id,
                    'name':name,
                    'contact_number':contact_number,
                    'company':company,
                    'reason':reason,
                    'person_to_meet':person_to_meet,
                }
                message = get_template('mail.html').render(ctx)
                msg = EmailMessage(
                    f'{name} awaiting security clearance !!',
                    message,
                    'harshitaagarwal219@gmail.com',
                    [person_to_meet],
                )
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send()
                return redirect('.')

            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse('Try Again !!')

    def get_context_data(self, **kwargs):
        context = super(VisitorFormView, self).get_context_data(**kwargs)
        context['form_1'] = self.form_1
        return context

class DemoBootstrap3(VisitorFormView):
    template_name = 'demo/demo_bootstrap_3.html'

    def __init__(self, *args, **kwargs):
        # For this case we must set DJANGO_POPUP_VIEW_FIELD_TEMPLATE_PACK
        settings.DJANGO_POPUP_VIEW_FIELD_TEMPLATE_PACK = 'bootstrap3'
        super(DemoBootstrap3, self).__init__(*args, **kwargs)

def visitor_meet_yes(request, pk):
    try:
        user_details = get_object_or_404(VisitorManagementForm, pk=pk)
        if user_details.is_approved == None:
            to_update = VisitorManagementForm.objects.filter(id=pk).update(is_approved=True)
            return JsonResponse({'Message': "The Visit has been approved !!"})
        else:
            return JsonResponse({'Message': "Request can be access only one time"})
    except visitor_meet_yes.DoesNotExist:
        raise Http404

def visitor_meet_no(request, pk):
    try:
        user_details = get_object_or_404(VisitorManagementForm, pk=pk)
        if user_details.is_approved == None:
            to_update = VisitorManagementForm.objects.filter(id=pk).update(is_approved=False)
            return JsonResponse({'Message': "The Visit has been rejected !!"})
        else:
            return JsonResponse({'Message': "Request can be access only one time"})
    except Board.DoesNotExist:
        raise Http404


def all_visitors_list(request):
    visitors = VisitorManagementForm.objects.all().order_by('-id')
    return render(request,'visitor_list.html',{'visitors':visitors})


def rejected_visitor(request):
    visitors = VisitorManagementForm.objects.filter(is_approved=False)
    return render(request,'rejected_visitor_list.html',{'visitors':visitors})


def approved_visitor(request):
    visitors = VisitorManagementForm.objects.filter(is_approved=True)
    return render(request,'approved_visitor_list.html',{'visitors':visitors})

def sendmail(request):
    # name=request.session.get('name')
    # contact_number=request.session.get('contact_number')
    # company=request.session.get('company')
    # person_to_meet=request.session.get('person_to_meet')
    # reason=request.session.get('reason')
    # print(name,'mmmmmmmmmmmmmmmmmmmmmmmmmmmmjjjjjjjjjjjjjjjjjjjmm')
    ctx = {
        'name': 'Harshita',
        'contact_number': '8393944951',
        'company': 'C&S',
        'reason': 'Meeting',
        'person_to_meet': 'aharshita31@gmail.com',
    }
    message = get_template('mail_11.html').render(ctx)
    msg = EmailMessage(
        'Harshita awaiting security clearance !!',
        message,
        'harshitaagarwal219@gmail.com',
        ['aharshita31@gmail.com'],
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()


    return redirect("/vms")

def test(request):
    return render(request,'click-to-run.html')