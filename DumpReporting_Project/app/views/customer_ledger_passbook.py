from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import xlsxwriter
import cx_Oracle
from io import BytesIO, StringIO
from app.forms import CustomerLdgerPassbookForm1, CustomerLdgerPassbookForm2
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import psycopg2
from django.contrib import messages
from django.db import connection
from datetime import datetime
from django.contrib.auth.decorators import permission_required,login_required
import re
from app.db import oracle_db_connection
from django.views.generic import FormView
from django.conf import settings
from itertools import zip_longest, chain
import time as t
import codecs
from codecs import open



# @login_required
class DemoBase(FormView):
    form_class = CustomerLdgerPassbookForm1
    form_1 = None

    def get(self, request, *args, **kwargs):
        self.form_1 = self.form_class(prefix='form_1')
        return super(DemoBase, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.form_1 = self.form_class(prefix='form_1', data=request.POST)
        if self.form_1.is_valid():
            form1 = self.form_1.save(commit=False)
            organisation = self.form_1.cleaned_data['organisation']
            request.session['organisation'] = organisation

            res = organisation[4:]
            p_org_id = re.sub(r'\,.*', "", res)
            customer = self.form_1.cleaned_data['customer']
            res1 = customer[4:]
            p_cus_id = re.sub(r'\,.*', "", res1)
            self.form_1.save()
            return redirect(f'/clp/{p_org_id}/{p_cus_id}/')
        else:
            return HttpResponse('Try again')

    def get_context_data(self, **kwargs):
        context = super(DemoBase, self).get_context_data(**kwargs)
        context['form_1'] = self.form_1
        return context


class DemoBootstrap3(DemoBase):
    template_name = 'demo/demo_bootstrap_3.html'

    def __init__(self, *args, **kwargs):
        # For this case we must set DJANGO_POPUP_VIEW_FIELD_TEMPLATE_PACK
        settings.DJANGO_POPUP_VIEW_FIELD_TEMPLATE_PACK = 'bootstrap3'
        super(DemoBootstrap3, self).__init__(*args, **kwargs)


class Form2(FormView):
    form_class = CustomerLdgerPassbookForm2
    form_1 = None

    def get(self, request, *args, **kwargs):
        request.session['p_org_id'] = kwargs['p_org_id']
        request.session['p_cus_id'] = kwargs['p_cus_id']
        self.form_1 = self.form_class(prefix='form_1')
        return super(Form2, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.form_1 = self.form_class(prefix='form_1', data=request.POST)
        if self.form_1.is_valid():
            form1 = self.form_1.save(commit=False)
            customer_number = self.form_1.cleaned_data['customer_number']
            customer_site = self.form_1.cleaned_data['customer_site']
            customer_type = self.form_1.cleaned_data['customer_type']
            start_date = self.request.POST.get('s_date')
            end_date = self.request.POST.get('e_date')
            self.form_1.save()
            return HttpResponseRedirect('.')
        else:
            return HttpResponse('Try again')

    def get_context_data(self, **kwargs):
        context = super(Form2, self).get_context_data(**kwargs)
        context['form_1'] = self.form_1
        return context

class Form2Bootstrap3(Form2):
    template_name = 'demo/form2_bootstrap_3.html'

    def __init__(self, *args, **kwargs):
        # For this case we must set DJANGO_POPUP_VIEW_FIELD_TEMPLATE_PACK
        settings.DJANGO_POPUP_VIEW_FIELD_TEMPLATE_PACK = 'bootstrap3'
        super(Form2Bootstrap3, self).__init__(*args, **kwargs)

def data_save(request):
    customer= request.session.get('customer')
    f = open('customer_no.txt', 'w')
    f.write(str(customer))
    f.close()
    return HttpResponse('Done')


@api_view(['POST'])
def download_customer_ledger_passbook(request):
    '''
    Download the report from postgres database
    :param request:
    :return:
    '''
    data = request.data
    organisation =request.session.get('organisation')
    p_customer_id = request.session.get('p_cus_id')
    p_org_id = request.session.get('p_org_id')
    form_1_customer_site = data['form_1-customer_site']
    res1 = form_1_customer_site[4:]
    P_CUSTOMER_SITE = re.sub(r'\,.*', "", res1)
    p_customer_type = data['form_1-customer_type']
    start_date = data['s_date']
    end_date = data['e_date']
    p_end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime('%d-%b-%Y')
    p_start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime('%d-%b-%Y')
    dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
    conn_ora = cx_Oracle.connect(user=r'apps', password='apps1234', dsn=dsn_tns)
    cursor_ora = conn_ora.cursor()
    p_customer_id2= p_customer_id
    # p_end_date = '08-JUN-2020' 01-JUN-2019
    # p_org_id = 105
    sql_statement = open('app/QueriesFolder/header_query.sql').read()
    header_query =sql_statement.replace('{p_customer_id}', p_customer_id).replace('{p_customer_id2}',p_customer_id2).\
        replace('{p_customer_type}',p_customer_type).replace('{P_CUSTOMER_SITE}', P_CUSTOMER_SITE).\
        replace('{p_end_date}',p_end_date).replace('{p_start_date}',p_start_date).replace('{p_org_id}',p_org_id)
    t.sleep(1)
    cur = cursor_ora.execute(str(header_query))
    customer_report = cur.fetchall()
    line_statement = open('app/QueriesFolder/line_query.sql').read()
    line_query = line_statement.replace('{p_customer_id}', p_customer_id).replace('{p_customer_id2}', p_customer_id2). \
        replace('{p_customer_type}', p_customer_type).replace('{P_CUSTOMER_SITE}', P_CUSTOMER_SITE). \
        replace('{p_end_date}', p_end_date).replace('{p_start_date}', p_start_date).replace('{p_org_id}', p_org_id)
    t.sleep(1)

    cur_data = cursor_ora.execute(line_query)
    line_query_data = cur_data.fetchall()
    output = BytesIO()
    for header in customer_report:
        name = header[0]
        id = header[3]
        customer_no = header[1]
        customer_type_ =header[2]
        currency_code = header[4]
        customer_site_id = header[5]
        opening_statement = open('app/QueriesFolder/opening_query.sql').read()
        opening_query = opening_statement.replace('{p_customer_id}', p_customer_id).\
            replace('{currency_code}', currency_code).replace('{p_start_date}', p_start_date).replace('{p_org_id}', p_org_id)
        t.sleep(1)
        cur_data = cursor_ora.execute(opening_query)
        opening_query_data = cur_data.fetchall()
        opening_data = str(opening_query_data).replace('[(','').replace(',)]','')
        list_running = []
        i = 0
        while i < len(line_query_data):
            running_balance = float(opening_data) + line_query_data[i][4] - line_query_data[i][5]
            opening_data = running_balance
            i += 1
            list_running.append(running_balance)
        try:
            running_query_val = list(map(lambda el: [el], list_running))
            closing_bal = [running_query_val[-1]]
            print(closing_bal,'dddddddddddddddddddddddddddddddddddddddddddddd')
        except:
            closing_bal = [[0]]
        workbook = xlsxwriter.Workbook(output)
        worksheet1 = workbook.add_worksheet()
        row_count = 23
        column_count = 1
        caption = 'Passbook'
        bold = workbook.add_format({'bold': True})
        format = workbook.add_format()
        format.set_font_size(25)
        worksheet1.insert_image('D1', 'app/static/logo.jpg', {'x_scale': 0.5, 'y_scale': 0.5})
        worksheet1.write('C5', 'Customer Ledger Passbook', format)

        # Some sample data for the table.
        data = [
            ['Organization Deatils', organisation],
            ['Customer Id', id],
            ['Customer Name', name],
            ['Customer No', customer_no],
            ['Currency Code', currency_code],
            ['Customer Site Address', customer_site_id],
            ['Customer TYPE', customer_type_],
            ['Date From', p_start_date],
            ['Date To', p_end_date],
        ]

        # Write the caption.
        worksheet1.add_table('B7:C16', {'data': data or None})

        worksheet1.add_table('G20:G21', {'data': opening_query_data,
                                         'columns': [{'header': 'Opening Balance'},
                                                     ]})
        table_row_count = row_count + (len(line_query_data) or 1)
        col_count = 8
        worksheet1.add_table(row_count, col_count,
                             table_row_count, 8,
                             {'data': running_query_val,
                              'columns': [{'header': 'Running Balance'},
                                          ]})

        table_headers = worksheet1.add_table(row_count, column_count,
             table_row_count, 7, {'data': line_query_data,
                                        'columns': [{'header': 'Document No.'},
                                                    {'header': 'Document Date'},
                                                    {'header': 'Document Type'},
                                                    {'header': 'Reference'},
                                                    {'header': 'Debit'},
                                                    {'header': 'Credit'},
                                                    {'header': 'Remarks'},
                                                    ]})

        row1_count = table_row_count + 3
        table_row_count_1 = row1_count + 2
        column_count_ = 6
        worksheet1.add_table(row1_count, column_count_,
                             table_row_count_1, 6, {'data': closing_bal,
                                                    'columns': [{'header': 'Closing Balance'}
                                                                ]})
        workbook.close()
        output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    return response
