from django.shortcuts import redirect, render_to_response, get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from .forms import VisitorManagementFormCreate, VisitorManagementExcelRepot,MobileRegisteredForm, VistiorsFormFrequent
from django.views.generic import TemplateView, ListView
from .models import VisitorManagementForm, MobileRegistered, FrequentVisitors
from django.conf import settings
from rest_framework.decorators import api_view
from io import BytesIO, StringIO
import xlsxwriter
from django.template.loader import render_to_string, get_template
from easy_pdf.views import PDFTemplateView
from django.core.mail import EmailMessage
import datetime
from django.http import Http404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.db.models import Q
from xhtml2pdf import pisa
from io import StringIO
from django.template.loader import get_template
from django.template import Context

x = datetime.datetime.now()
image_click_date = x.strftime("%d-%m-%Y_%I-%M-%S_%p")
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator


class FrequentVisitorsForm(TemplateView):
    '''
    Frequent Visitor Create Form
    Registration Form of frequent Visitor
    '''
    form_class = VistiorsFormFrequent
    form_1 = None

    # @method_decorator(permission_required('app.view_security_form'))
    def get(self, request, *args, **kwargs):
        self.form_1 = self.form_class(prefix='form_1')
        return super(FrequentVisitorsForm, self).get(request, *args, **kwargs)

    # @method_decorator(permission_required('app.view_security_form'))
    def post(self, request, *args, **kwargs):
        self.form_1 = self.form_class(prefix='form_1', data=request.POST)
        if self.form_1.is_valid():
            form_db = self.form_1.save(commit=False)
            x = datetime.datetime.now()
            date = x.strftime("%Y-%m-%d")
            time = x.strftime("%H:%M:%S  %p")
            visitor_name =self.form_1.cleaned_data['visitor_name']
            self.request.session['visitor_name'] = visitor_name
            mobile_number = self.form_1.cleaned_data['mobile_number']
            if mobile_number in FrequentVisitors.objects.filter(mobile_number=mobile_number):
                messages.error(request, 'The Mobile Number is registered')
            self.request.session['mobile_number'] = mobile_number
            company = self.form_1.cleaned_data['company']
            host_department = self.form_1.cleaned_data['host_department']
            host_name = self.form_1.cleaned_data['host_name']
            visitor_valid_upto = self.form_1.cleaned_data['visitor_valid_upto']
            pic_data = os.rename(os.path.join(f"ImageFolder/Frequent_visitor.png"), os.path.join(f"ImageFolder/frequent_visitor{mobile_number}_and_{image_click_date}.png"))
            pic = f"/ImageFolder/frequent_visitor{mobile_number}_and_{image_click_date}.png"
            reason = self.form_1.cleaned_data['reason']
            p = FrequentVisitors(visitor_name=visitor_name, mobile_number=mobile_number, company=company,
                                      host_department=host_department, host_name=host_name,
                                 visitor_valid_upto=visitor_valid_upto,pic=pic,reason=reason,
                                 visitor_registration_date=date , visitor_time=time)
            p.save()
            # have to change Url when will be upload in server
            url_create_yes = f'http://127.0.0.1:8000/fv/{p.id}/y'
            url_create_no = f'http://127.0.0.1:8000/fv/{p.id}/n'
            image_file = open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + f'{pic}','rb')  # get the image file
            msg_image = MIMEImage(image_file.read())  # with proper MIME type
            image_file.close()
            ctx = {
                'url_create_yes': url_create_yes,
                'url_create_no': url_create_no,
                'visit_id': p.id,
                'visitor_name': visitor_name,
                'mobile_number': mobile_number,
                'company': company,
                'host_department': host_department,
                'host_name': host_name,
                'visitor_valid_upto':visitor_valid_upto,
                # 'pic': '../'+ pic,
                # 'image_file':image_file,
                'reason':reason,
            }
            message = get_template('frequent_visitor_mail.html').render(ctx)
            msg = EmailMultiAlternatives(
                f'{visitor_name} awaiting security clearance !!',
                message,
                'harshitaagarwal219@gmail.com',  # will be change
                [host_name],
            )
            msg.content_subtype = "html"  # Main content is now text/html
            msg.attach(msg_image)
            msg.send()
            return redirect('.')
        else:
            return HttpResponse(self.form_1.errors)

    def get_context_data(self, **kwargs):
        context = super(FrequentVisitorsForm, self).get_context_data(**kwargs)
        context['form_1'] = self.form_1
        return context


class FrequentVisitorsFormData(FrequentVisitorsForm):
    '''
    Frequent Visitor Form Template call (Main Method)
    '''
    template_name = 'demo/visitor_frequent_form.html'

    def __init__(self, *args, **kwargs):
        # For this case we must set DJANGO_POPUP_VIEW_FIELD_TEMPLATE_PACK
        settings.DJANGO_POPUP_VIEW_FIELD_TEMPLATE_PACK = 'bootstrap3'
        super(FrequentVisitorsFormData, self).__init__(*args, **kwargs)


class VisitorFormView(TemplateView):
    '''
    Visitor Form

    '''
    form_class = VisitorManagementFormCreate
    form_1 = None

    # @method_decorator(permission_required('app.view_host_form'))
    def get(self, request, *args, **kwargs):
        self.form_1 = self.form_class(prefix='form_1')
        return super(VisitorFormView, self).get(request, *args, **kwargs)

    # @method_decorator(permission_required('app.view_host_form'))
    def post(self, request, *args, **kwargs):
        self.form_1 = self.form_class(prefix='form_1', data=request.POST)
        if self.form_1.is_valid():
            try:
                form_db = self.form_1.save(commit=False)
                x = datetime.datetime.now()
                date = x.strftime("%Y-%m-%d")
                time = x.strftime("%H:%M:%S  %p")
                name =self.form_1.cleaned_data['name']
                self.request.session['name'] = name
                contact_number = self.form_1.cleaned_data['contact_number']
                self.request.session['contact_number'] = contact_number
                company = self.form_1.cleaned_data['company']
                pic_data = os.rename(os.path.join(f"ImageFolder/Profile.png"),
                                  os.path.join(f"ImageFolder/visitor{contact_number}_and_{image_click_date}.png"))
                pic = f"/ImageFolder/visitor{contact_number}_and_{image_click_date}.png"
                self.request.session['company'] = company
                person_to_meet = self.form_1.cleaned_data['person_to_meet']
                self.request.session['person_to_meet'] = person_to_meet
                reason = self.form_1.cleaned_data['reason']
                self.request.session['reason'] = reason
                p = VisitorManagementForm(name=name, contact_number=contact_number, company=company,
                                          person_to_meet=person_to_meet, reason=reason,v_date_time=date,pic=pic, visitor_time=time)
                p.save()
                # have to change Url when will be upload in server
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
                image_file = open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + f'{pic}',
                                  'rb')  # get the image file
                msg_image = MIMEImage(image_file.read())  # with proper MIME type
                image_file.close()
                message = get_template('mail_copy1.html').render(ctx)
                msg = EmailMessage(
                    f'{name} awaiting security clearance !!',
                    message,
                    'harshitaagarwal219@gmail.com', # will be change
                    [person_to_meet],
                )
                msg.content_subtype = "html"  # Main content is now text/html
                msg.attach(msg_image)
                msg.send()
                return redirect('.')
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse(self.form_1.errors)

    def get_context_data(self, **kwargs):
        context = super(VisitorFormView, self).get_context_data(**kwargs)
        context['form_1'] = self.form_1
        return context


class DemoBootstrap3(VisitorFormView):
    '''
    Main Visitor Form , Template Called
    '''
    template_name = 'demo/demo_bootstrap_3.html'

    def __init__(self, *args, **kwargs):
        # For this case we must set DJANGO_POPUP_VIEW_FIELD_TEMPLATE_PACK
        settings.DJANGO_POPUP_VIEW_FIELD_TEMPLATE_PACK = 'bootstrap3'
        super(DemoBootstrap3, self).__init__(*args, **kwargs)


def frequent_visitor_meet_yes(request, pk):
    '''
    Frequent Visitor Who approved Yes by HOST
    :param request:
    :param pk:
    :return:
    '''
    try:
        user_details = get_object_or_404(FrequentVisitors, pk=pk)
        if user_details.is_approved == None:
            to_update = FrequentVisitors.objects.filter(id=pk).update(is_approved=True)
            return JsonResponse({'Message': "The Visit has been approved !!"})
        else:
            return JsonResponse({'Message': "Request can be access only one time"})
    except ObjectDoesNotExist:
        raise Http404


def frequent_visitor_meet_no(request, pk):
    '''
    Frequent Visitor Form Who did not approve!!
    :param request:
    :param pk:
    :return:
    '''
    try:
        user_details = get_object_or_404(FrequentVisitors, pk=pk)
        if user_details.is_approved == None:
            to_update = FrequentVisitors.objects.filter(id=pk).update(is_approved=False)
            return JsonResponse({'Message': "The Visit has been rejected !!"})
        else:
            return JsonResponse({'Message': "Request can be access only one time"})
    except ObjectDoesNotExist:
        raise Http404


def punch_in_details(request):
    '''
    Frequent User Punch In Form based on registration
    Visitor who has been approved and visitor valid date grater then current sys data then visitor can punch in..
    Otherwise Can not Punch In....
    :param request:
    :return:
    '''
    form =MobileRegisteredForm(request.POST or None)
    if form.is_valid():
        form_1 = form.save(commit=False)
        mobile_number = form.cleaned_data['mobile_number']
        x = datetime.datetime.now()
        date = x.strftime("%Y-%m-%d %H:%M:%S")
        date1 = x.strftime("%Y-%m-%d")
        check_mobile_number = FrequentVisitors.objects.filter(mobile_number=mobile_number)
        if not check_mobile_number:
            messages.error(request, 'Mobile Number is not registered')
        else:
            cursor = connection.cursor()
            table_name = 'app_frequentvisitors'
            data = f"SELECT * FROM {table_name} WHERE mobile_number LIKE '{mobile_number}';"
            cursor.execute(data)
            row = cursor.fetchall()
            for i in row:
                if i[6] >= date1:
                    if i[9] ==True:
                        create_attendance = VisitorManagementForm(name=i[1], contact_number=i[2], company=i[3],
                                                                  person_to_meet=i[5], reason='Frequent User',
                                                                  v_date_time=date, is_approved=i[9], Approved_by='Self')
                        create_attendance.save()
                        messages.success(request, f'You have logged in at {date} !!!')
                    else:
                        messages.error(request, 'Approval Request is Not Approved yet!!')
                else:
                    messages.error(request, 'valid date has been expired !! You can not Login')
            return redirect('/punch_in')
    return render(request,'punch_in_detail.html',{'form':form})


def all_visitors_list(request):
    '''
     All Visitor Form View , To Show All the Visitors Data
     Also Search data based on name, mobile number..
    :param request:
    :return:
    '''
    visitors = VisitorManagementForm.objects.all().order_by('-id')
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            visitors = VisitorManagementForm.objects.filter(Q(name__istartswith=query) | Q(contact_number__istartswith=query)
                                            | Q(v_date_time__istartswith=query) | Q(Approved_by__istartswith=query)
                                         | Q(person_to_meet__istartswith=query) | Q(company__istartswith=query))
            if visitors:
                return render(request, 'visitor_list.html', {'visitors': visitors})
            else:
                return JsonResponse({'Message': "No Data Found with this Search !!!"})
        else:
            visitors = VisitorManagementForm.objects.all().order_by('-id')
    return render(request,'visitor_list.html',{'visitors':visitors})


def security_approve(request, pk):
    '''
    Approval By Security , A security Person can approve the requets of visitor ...used in all_visitors_list method
    :param request:
    :param pk:
    :return:
    '''
    user_details = get_object_or_404(VisitorManagementForm, pk=pk)
    update_data_from_scurity_side = VisitorManagementForm.objects.filter(id=pk)
    cursor = connection.cursor()
    table_name = 'app_visitormanagementform'
    data = f"SELECT * FROM {table_name} WHERE id = '{pk}';"
    cursor.execute(data)
    row = cursor.fetchall()
    for i in row:
        if i[5] == None:
            update_approve = VisitorManagementForm.objects.filter(id=pk).update(is_approved=True, Approved_by='Security')
        # elif i[5] is not None:
        #     messages.error(request, 'Approve Action has been taken previously, Can not Update Again')
    return redirect('/visitor_list')


def visitor_meet_yes(request, pk):
    '''
    Visitor approval approved form!!
    :param request:
    :param pk:
    :return:
    '''
    try:
        user_details = get_object_or_404(VisitorManagementForm, pk=pk)
        if user_details.is_approved == None:
            to_update = VisitorManagementForm.objects.filter(id=pk).update(is_approved=True, Approved_by='Host')
            return JsonResponse({'Message': "The Visit has been approved !!"})
        else:
            return JsonResponse({'Message': "The visit has already been approved"})
    except visitor_meet_yes.DoesNotExist:
        raise Http404


def visitor_meet_no(request, pk):
    '''
    Visitor approval reject form
    :param request:
    :param pk:
    :return:
    '''
    try:
        user_details = get_object_or_404(VisitorManagementForm, pk=pk)
        if user_details.is_approved == None:
            to_update = VisitorManagementForm.objects.filter(id=pk).update(is_approved=False)
            return JsonResponse({'Message': "The Visit has been rejected !!"})
        else:
            return JsonResponse({'Message': "The visit has already been approved"})
    except visitor_meet_no.DoesNotExist:
        raise Http404


def rejected_visitor(request):
    visitors = VisitorManagementForm.objects.filter(is_approved=False)
    return render(request,'rejected_visitor_list.html',{'visitors':visitors})


def approved_visitor(request):
    visitors = VisitorManagementForm.objects.filter(is_approved=True)
    return render(request,'approved_visitor_list.html',{'visitors':visitors})

import cv2
import time
import getpass
import os


def normal_visitor_image(request):
    contact_number = request.session.get('contact_number')
    video_capture = cv2.VideoCapture(0)
    cv2.namedWindow("Window")
    while True:
        ret, frame = video_capture.read()
        cv2.imshow("Window", frame)
        cv2.imwrite(os.path.join(f"ImageFolder/Profile.png"), frame)
        # This breaks on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
    return HttpResponse('Visitor  Profile is created')


def frequent_vistor_image(request):
    mobile_number = request.session.get('mobile_number')
    video_capture = cv2.VideoCapture(0)
    cv2.namedWindow("Window")
    while True:
        ret, frame = video_capture.read()
        cv2.imshow("Window", frame)
        path = f'ImageFolder/Frequent_visitor.png'
        cv2.imwrite(os.path.join(path), frame)
        # This breaks on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
    return HttpResponse('Frequent Visitor  Profile is created')


class VisitorCardPrintView(PDFTemplateView):
    template_name = "visitor_idcard_pdf.html"

    def get_context_data(self, **kwargs):
        data = []
        context =super(VisitorCardPrintView, self).get_context_data(
            pagesize="A6",
            title="Employee ID Card",
            **kwargs
            )
        myinstance = get_object_or_404(VisitorManagementForm, pk=context['pk'])
        id = myinstance.id
        table_name = 'app_visitormanagementform'
        cursor = connection.cursor()
        data = f"SELECT * FROM {table_name} WHERE id = {id};"
        cursor.execute(data)
        row = cursor.fetchall()
        for i in row:
            name = i[1]
            host_name= i[4]
            in_time = i[7]
            pic = i[8]
            context['myinstance'] = myinstance
            context['name'] = name
            context['id'] = id
            context['host_name'] = host_name
            context['in_time'] = in_time
            return context


def create_vms_report(request):
    form =VisitorManagementExcelRepot(request.POST or None)
    if form.is_valid():
        data = form.save(commit=False)
        form.save()
        return redirect('')
    return render(request,'vms_report_excel.html', {'form': form})


@api_view(['POST'])
def download_vms_report(request):
    '''
    Download the report from postgres database
    :param request:
    :return:
    '''
    data = request.data
    name = data['name']
    contact_number = data['contact_number']
    person_to_meet = data['person_to_meet']
    from_date = data['from_date']
    to_date = data['to_date']
    cursor = connection.cursor()
    TABLE_NAME = 'app_visitormanagementform'
    sql_statement = f'''SELECT * FROM {TABLE_NAME} WHERE  ('{name}'='' OR name = '{name}') and ('{contact_number}'='' OR
contact_number = '{contact_number}') and  ('{person_to_meet}'='' OR person_to_meet = '{person_to_meet}') and
v_date_time BETWEEN '{from_date}' AND  '{to_date}';
'''
    cursor.execute(sql_statement)
    row_data = cursor.fetchall()
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'constant_memory': True})
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})
    headings = ['Id','Name','Contact Number' ,'Company','Person To Meet','Is Approved','Reason For Meeting','Date',
                'Pic','Approved By','Time']
    col = 0
    for row, data in enumerate(row_data):
        worksheet.write_row('A1', headings, bold)
        worksheet.write_row(row+1, col, data)
    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    return response






























# class SearchResultsView(ListView):
#     model = VisitorManagementForm
#     template_name = 'search_results.html'
#
#     def get_queryset(self):
#         return VisitorManagementForm.objects.filter(name='Puneet Kumar')