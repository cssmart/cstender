from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import xlsxwriter
import cx_Oracle
from io import BytesIO, StringIO
from app.forms import CustomerLedgerPassbookForm
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import psycopg2
from django.contrib import messages
from django.db import connection
from datetime import datetime
import re
from app.db import oracle_db_connection
from django.views.generic import FormView
from django.conf import settings


class DemoBase(FormView):
    form_class = CustomerLedgerPassbookForm
    form_1 = None

    def get(self, request, *args, **kwargs):
        self.form_1 = self.form_class(prefix='form_1')
        return super(DemoBase, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.form_1 = self.form_class(prefix='form_1', data=request.POST)
        if self.form_1.is_valid():
            form1 = self.form_1.save(commit=False)
            organisation = self.form_1.cleaned_data['organisation']
            customer = self.form_1.cleaned_data['customer']
            if 'save' in self.request.POST.get():
                f = open('customer_no.txt', 'w')
                f.write(str(customer))
                f.close()
                return HttpResponse('Done')

            form1.save()
            self.request.session['customer'] = customer

            self.request.session.save()
            print(self.request.session,'ddddddddddddddddddddddddddddd==========================')

            customer_number = self.form_1.cleaned_data['customer_number']
            customer_site = self.form_1.cleaned_data['customer_site']
            customer_type = self.form_1.cleaned_data['customer_type']
            start_date = self.request.POST.get('s_date')
            print(start_date,'xxxxxxxxxxxxxxxxxxxxxx')
            end_date = self.request.POST.get('e_date')
            print(end_date,'wwwwwwwwwwwwwwwwwwwwwww')
            form1.save()
            return HttpResponseRedirect('.')
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


def data_save(request):
    customer= request.session.get('customer')
    print(customer,'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
    f = open('customer_no.txt', 'w')
    f.write(str(customer))
    f.close()
    return HttpResponse('Done')

@api_view(['POST'])
def download_customer_passbook(request):
    data = request.data
    print(data, 'daa========================')
    form_1_organisation = data['form_1-organisation']
    res = form_1_organisation[4:]
    p_org_id = re.sub(r'\,.*', "", res)
    form_1_customer = data['form_1-customer']
    res1 = form_1_customer[4:]
    p_customer_id = re.sub(r'\ ,.*', "", res1)
    P_CUSTOMER_SITE = data['form_1-customer_site']
    p_customer_type = data['form_1-customer_type']
    start_date = data['s_date']
    end_date = data['e_date']
    p_customer_id2 = p_customer_id
    p_end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime('%d-%b-%Y')
    p_start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime('%d-%b-%Y')
    dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
    conn_ora = cx_Oracle.connect(user=r'apps', password='apps1234', dsn=dsn_tns)
    cursor_ora = conn_ora.cursor()
    print(conn_ora, '2222222222222222')
    line_query = f'''Select
           hzca.cust_account_id  customer_id,
            B.BILL_TO_SITE_USE_ID customer_site_id,
           hzca.account_number customer_number   ,
           a.party_name   customer_name                             ,
           d.gl_date                                                ,
           B.CUSTOMER_TRX_ID                                        ,
           b.trx_number                                             ,
           (SELECT interface_line_Attribute1
           FROM ra_customer_Trx_lines_All
           where CUSTOMER_TRX_ID=b.CUSTOMER_TRX_ID
           and org_id=b.org_id
           and rownum=1)reference,
           TO_CHAR(b.trx_date, 'DD-MM-YYYY') trx_date               ,
           NULL receipt_number                                      ,
           NULL receipt_date                                        ,
           SUBSTR(b.comments,1,50) remarks                          ,
           d.code_combination_id account_id                         ,
           b.invoice_currency_code currency_code                    ,
           b.exchange_rate                                          ,
           d.amount amount                                          ,
           (d.amount * NVL(b.exchange_rate,1)) amount_other_currency,
           F.TYPE                                          ,
           xxcns_deb_led_get_narration(F.TYPE,F.NAME,B.CUSTOMER_TRX_ID)naration,
           b.customer_trx_id                                        ,
           d.customer_trx_line_id                                   ,
           b.rowid
           From
              hz_parties                                           a,
              hz_cust_accounts                                     hzca,
              ra_customer_trx_ALL                                  B,
              RA_CUST_TRX_LINE_GL_DIST_ALL                         D,
              GL_CODE_COMBINATIONS                                 E,
              RA_CUST_TRX_TYPES_ALL                                F,
              ar_payment_schedules_all                             G,
              hz_locations                                         loc,
              hz_party_sites                                       party_site,
              hz_cust_acct_sites_all                               acct_site,
              hz_cust_site_uses_all                                site
           Where a.party_id = hzca.party_id
           AND   b.bill_to_customer_id = hzca.cust_account_id
           AND      b.complete_flag       = 'Y'
           AND     d.customer_trx_id     = b.customer_trx_id
           AND     d.account_class       = 'REC'
           AND     e.code_combination_id = d.code_combination_id
           AND    f.cust_trx_type_id    = b.cust_trx_type_id
           AND     f.type in ('INV','CM','DM','DEP')
           AND     d.latest_rec_flag     = 'Y'
           AND     g.customer_trx_id     = b.customer_trx_id
           and   loc.location_id       = party_site.location_id
           and   party_site.party_site_id    = acct_site.party_site_id
           and   acct_site.cust_acct_site_id = site.cust_acct_site_id
           and   site.site_use_id            = g.customer_site_use_id
           AND     b.org_id              ='{p_org_id}'
           AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
           AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
           AND   NVL(b.BILL_TO_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(b.BILL_TO_SITE_USE_ID,'99999999999999'))
           AND      to_date(g.gl_date,'DD-MON-RRRR') between  to_date('{p_start_date}','DD-MON-RRRR')  AND to_date('{p_end_date}','DD-MON-RRRR')
           AND b.invoice_currency_code='INR'
           and     g.payment_schedule_id in
           (select min(payment_schedule_id)
            from   ar_payment_schedules_all
            where  customer_trx_id = g.customer_trx_id)
           UNION
           -- Following Query for Cash receipts
           Select
           hzca.cust_account_id customer_id,
            F.CUSTOMER_SITE_USE_ID customer_site_id ,
           hzca.account_number  customer_number   ,
           a.party_name customer_name                               ,
           e.gl_date                                                ,
           0                                                        ,
           b.receipt_number                                                   ,
           NULL                                                     ,
           TO_CHAR(b.receipt_date,  'DD-MM-YYYY'),
           b.receipt_number                                        ,
           TO_CHAR(b.receipt_date,  'DD-MM-YYYY')                   ,
           NULL                                                     ,
           d.cash_ccid account_id                                   ,
           b.currency_code                                          ,
           b.exchange_rate                                          ,
           b.amount  amount                                         ,
           (b.amount * NVL(b.exchange_rate,1)) amount_other_currency,
           'REC' type                                               ,
           'Amount Received' naration,
           0                                                        ,
           0                                                        ,
           b.rowid
           From
               hz_parties a, hz_cust_accounts hzca,
               ar_cash_receipts_all                                B,
               gl_code_combinations                                C,
               ar_receipt_method_accounts_all                      D,
               ar_cash_receipt_history_all                         E,
                       ar_payment_schedules_all                            F
           Where a.party_id = hzca.party_id
           AND b.pay_from_customer                     = hzca.cust_account_id
           AND    b.remit_bank_acct_use_id            = d.remit_bank_acct_use_id
           AND         d.receipt_method_id                     = b.receipt_method_id
           AND    d.cash_ccid                             = c.code_combination_id
           AND         e.cash_receipt_id                       = b.cash_receipt_id
           AND E.cash_receipt_history_id in (SELECT    min(incrh.cash_receipt_history_id)
                                                         FROM    ar_cash_receipt_history_all incrh
                                                         WHERE   incrh.cash_receipt_id = B.cash_receipt_id
                                                         AND     incrh.status <> 'REVERSED' )
           AND     f.cash_receipt_id                           = b.cash_receipt_id
           AND     b.org_id                                   ='{p_org_id}'
           AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
           AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
           AND   NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999'))
           AND    to_date(e.gl_date,'DD-MON-RRRR') between to_date('{p_start_date}','DD-MON-RRRR')  AND to_date('{p_end_date}','DD-MON-RRRR')
           AND b.currency_code ='INR'
           UNION
           -- Following Query for Receipt WriteOff
           Select
           hzca.cust_account_id customer_id  ,
            F.CUSTOMER_SITE_USE_ID customer_site_id                          ,
           hzca.account_number  customer_number,
           a.party_name customer_name ,
           g.gl_date     ,
           0                                                                ,
           b.receipt_number                                                             ,
           NULL ,
           TO_CHAR(b.receipt_date,  'DD-MM-YYYY'),
           b.receipt_number                                                 ,
           TO_CHAR(b.receipt_date,  'DD-MM-YYYY')                           ,
           NULL                                                             ,
           d.cash_ccid account_id                                           ,
           b.currency_code                                                  ,
           b.exchange_rate                                                  ,
           g.amount_applied  amount                                         ,
           (g.amount_applied * NVL(b.exchange_rate,1)) amount_other_currency,
           'W/O' type                                                       ,
           xxcns_deb_led_get_narration(TYPE,NULL,0)naration,
           0                                                                ,
           0                                                                ,
           b.rowid
           From
               hz_parties a, hz_cust_accounts hzca ,
               ar_cash_receipts_all                                        B,
               gl_code_combinations                                        C,
               ar_receipt_method_accounts_all                              D,
               ar_cash_receipt_history_all                                 E,
                   ar_payment_schedules_all                                    F,
                   ar_receivable_applications_all                              G
           Where a.party_id = hzca.party_id
           AND b.pay_from_customer                     = hzca.cust_account_id
           AND g.applied_payment_schedule_id           = -3
           AND g.cash_receipt_id                       = b.cash_receipt_id
           and g.cash_receipt_history_id               = e.cash_receipt_history_id
           AND g.status                                = 'ACTIVITY'
           AND    b.remit_bank_acct_use_id                = d.remit_bank_acct_use_id
           AND d.receipt_method_id                     = b.receipt_method_id
           AND    d.cash_ccid                             = c.code_combination_id
           AND e.cash_receipt_id                       = b.cash_receipt_id
           AND f.cash_receipt_id                       = b.cash_receipt_id
           AND b.org_id                                ='{p_org_id}'
           AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
           AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
           AND   NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999'))
           AND    to_date(g.gl_date,'DD-MON-RRRR')  between to_date('{p_start_date}','DD-MON-RRRR')  AND to_date('{p_end_date}','DD-MON-RRRR')
           AND b.currency_code ='INR'
           and not exists
           (select 1
            from   ar_cash_receipt_history_all
            where  cash_receipt_id = b.cash_receipt_id
            and    status = 'REVERSED'
            )
           UNION
           -- Following Query for Receipt WriteOff
           Select
           hzca.cust_account_id customer_id  ,
            F.CUSTOMER_SITE_USE_ID customer_site_id                          ,
           hzca.account_number customer_number           ,
           a.party_name customer_name                                       ,
           g.gl_date     ,
           0                                                                ,
           b.receipt_number                                                            ,
           NULL ,
           TO_CHAR(b.receipt_date,  'DD-MM-YYYY')                                                       ,
           b.receipt_number                                                 ,
           TO_CHAR(b.receipt_date,  'DD-MM-YYYY')                           ,
           NULL                                                             ,
           d.cash_ccid account_id                                           ,
           b.currency_code                                                  ,
           b.exchange_rate                                                  ,
           g.amount_applied  amount                                         ,
           (g.amount_applied * NVL(b.exchange_rate,1)) amount_other_currency,
           'REF' type                                                       ,
           xxcns_deb_led_get_narration(TYPE,NULL,0)naration,
           0                                                                ,
           0                                                                ,
           b.rowid
           From
               hz_parties a, hz_cust_accounts hzca ,
               ar_cash_receipts_all                                        B,
               gl_code_combinations                                        C,
               ar_receipt_method_accounts_all                              D,
               ar_cash_receipt_history_all                                 E,
                   ar_payment_schedules_all                                    F,
                   ar_receivable_applications_all                              G
           Where a.party_id = hzca.party_id
           AND b.pay_from_customer                     = hzca.cust_account_id
           AND g.applied_payment_schedule_id           = -8
           AND g.cash_receipt_id                       = b.cash_receipt_id
           and g.cash_receipt_history_id               = e.cash_receipt_history_id
           AND g.status                                = 'ACTIVITY'
           AND    b.remit_bank_acct_use_id                = d.remit_bank_acct_use_id
           AND d.receipt_method_id                     = b.receipt_method_id
           AND    d.cash_ccid                             = c.code_combination_id
           AND e.cash_receipt_id                       = b.cash_receipt_id
           AND f.cash_receipt_id                       = b.cash_receipt_id
           AND b.org_id                                ='{p_org_id}'
           AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
           AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
           AND   NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999'))
           AND    to_date(g.gl_date,'DD-MON-RRRR')  between to_date('{p_start_date}','DD-MON-RRRR')  AND to_date('{p_end_date}','DD-MON-RRRR')
           AND b.currency_code ='INR'
           and not exists
           (select 1
            from   ar_cash_receipt_history_all
            where  cash_receipt_id = b.cash_receipt_id
            and    status = 'REVERSED'
            )
           UNION
           -- Following Query for Receipt Reversal
           Select
           hzca.cust_account_id customer_id ,
            F.CUSTOMER_SITE_USE_ID customer_site_id,
           hzca.account_number customer_number           ,
           a.party_name customer_name                                       ,
           e.gl_date gl_date                                                ,
           0                                                                ,
           b.receipt_number ,
           NULL                                                             ,
           to_char(e.trx_date,'DD-MM-YYYY')  trx_date                       ,
           b.receipt_number                                                 ,
           TO_CHAR(b.receipt_date,  'DD-MM-YYYY')                           ,
           NULL                                                             ,
           c.code_combination_id account_id                                 ,
           b.currency_code                                                  ,
           b.exchange_rate                                                  ,
           b.amount amount                                                  ,
           (b.amount * NVL(b.exchange_rate,1)) amount_other_currency        ,
           'REV' type                                                       ,
           'Amount Reversed' naration,
           0                                                                ,
           0                                                                ,
           b.rowid
           From
               hz_parties a, hz_cust_accounts hzca ,
               ar_cash_receipts_all                                        B,
               gl_code_combinations                                        C,
               ar_receipt_method_accounts_all                              D,
               ar_cash_receipt_history_all                                 E,
                   ar_payment_schedules_all                                    F
           Where a.party_id = hzca.party_id
           AND b.pay_from_customer                       = hzca.cust_account_id
           AND    b.remit_bank_acct_use_id                = d.remit_bank_acct_use_id
           AND d.receipt_method_id                     = b.receipt_method_id
           AND    d.cash_ccid                             = c.code_combination_id
           AND e.cash_receipt_id                       = b.cash_receipt_id
           AND f.cash_receipt_id                       = b.cash_receipt_id
           AND b.org_id                                = '{p_org_id}'
           AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
           AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
           AND   NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999'))
           AND e.status                                = 'REVERSED'
           AND    to_date(e.gl_date,'DD-MON-RRRR') between to_date('{p_start_date}','DD-MON-RRRR')  AND to_date('{p_end_date}','DD-MON-RRRR')
           AND b.currency_code ='INR'
           and b.reversal_date is not null
           UNION
           -- Following Query for Adjustments
           SELECT
           HZCA.CUST_ACCOUNT_ID CUSTOMER_ID  ,
            C.BILL_TO_SITE_USE_ID customer_site_id                               ,
           hzca.account_number  CUSTOMER_NUMBER           ,
           A.PARTY_NAME CUSTOMER_NAME                                       ,
           B.GL_DATE                                                        ,
           0                                                                ,
           B.ADJUSTMENT_NUMBER                                              ,
           NULL,
           TO_CHAR(B.APPLY_DATE,'DD-MM-YYYY') trx_date                      ,
           NULL receipt_number                                              ,
           NULL receipt_date                                                ,
           SUBSTR(b.comments,1,50) remarks                                  ,
           b.code_combination_id account_id                                 ,
           c.invoice_currency_code currency_code                            ,
           c.exchange_rate                                                  ,
           b.amount amount                                                  ,
           (b.amount*NVL(c.exchange_rate,1)) amount_other_currency          ,
           'ADJ' type                                                       ,
           xxcns_deb_led_get_narration(TYPE,NULL,0)naration,
           0                                                                ,
           0                                                                ,
           b.rowid
           FROM
           HZ_PARTIES A, HZ_CUST_ACCOUNTS HZCA,
           ar_adjustments_all                                              b,
           ra_customer_trx_all                                             c,
           ar_payment_schedules_all                                        d,
           gl_code_combinations                                            e
           WHERE
                b.customer_trx_id                         = c.customer_trx_id
           AND a.party_id                              = hzca.party_id
           AND c.bill_to_customer_id                   = hzca.cust_account_id
           AND b.status                                = 'A'
           AND    e.code_combination_id                   = b.code_combination_id
           AND    b.payment_schedule_id                   = d.payment_schedule_id
           AND    b.customer_trx_id                       = d.customer_trx_id
           AND c.org_id                                ='{p_org_id}'
           AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
           AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
           AND   NVL(C.BILL_TO_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(C.BILL_TO_SITE_USE_ID,'99999999999999'))
           AND    to_date(b.gl_date,'DD-MON-RRRR') between to_date('{p_start_date}','DD-MON-RRRR')  AND to_date('{p_end_date}','DD-MON-RRRR')
           AND c.invoice_currency_code ='INR'
           AND b.customer_trx_id not in (select customer_trx_id from ar_adjustments_all where CHARGEBACK_CUSTOMER_TRX_ID is not NULL or created_from = 'REVERSE_CHARGEBACK') /*added by abezgam for bug#10228717*/
           UNION ALL   ----comment by zakaul  UNION
           -- -- Following Query for Discounts
           Select
           hzca.cust_account_id customer_id,
            B.BILL_TO_SITE_USE_ID customer_site_id                                        ,
           hzca.account_number  customer_number                 ,
           a.party_name customer_name                                              ,
           d.gl_date                                                               ,
           B.CUSTOMER_TRX_ID                                                       ,
           b.trx_number                                                            ,
           (SELECT interface_line_Attribute1
           FROM ra_customer_Trx_lines_All
           where CUSTOMER_TRX_ID=b.CUSTOMER_TRX_ID
           and org_id=b.org_id
           and rownum=1)reference,
           TO_CHAR(b.trx_date, 'DD-MM-YYYY') trx_date                              ,
           NULL receipt_number                                                     ,
           NULL receipt_date                                                       ,
           SUBSTR(b.comments,1,50) remarks                                         ,
           earned_discount_ccid account_id                                                            ,
            b.invoice_currency_code currency_code                                  ,
           b.exchange_rate                                                         ,
           d.EARNED_discount_taken amount                                          ,
           d.ACCTD_EARNED_DISCOUNT_TAKEN  amount_other_currency ,
           'DSC' type                                                              ,
           'Cash Discount' naration,
           b.customer_trx_id                                                       ,
           0                                                                       ,
           b.rowid
           From
               hz_parties a, hz_cust_accounts hzca ,
               ra_customer_trx_all                                                B,
               ar_receivable_applications_all                                     D
           Where a.party_id = hzca.party_id
           AND b.bill_to_customer_id                   = hzca.cust_account_id
           AND    b.complete_flag                         = 'Y'
           AND D.EARNED_DISCOUNT_TAKEN                 is not null
           and D.EARNED_DISCOUNT_TAKEN                 <> 0
           AND b.org_id                                = '{p_org_id}'
           AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
           AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
           AND   NVL(b.BILL_TO_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(b.BILL_TO_SITE_USE_ID,'99999999999999'))
           and b.customer_trx_id                       = d.applied_customer_trx_id
           and d.application_type                      = 'CASH'
           and d.display                               = 'Y'
           AND to_date(d.gl_date,'DD-MON-RRRR') between to_date('{p_start_date}','DD-MON-RRRR')  AND to_date('{p_end_date}','DD-MON-RRRR')
           AND B.invoice_currency_code ='INR'
           UNION ALL
           -- Following Query for Exchange Gain and Loss
           SELECT
           hzca.cust_account_id customer_id  ,
            B.BILL_TO_SITE_USE_ID customer_site_id                                       ,
           hzca.account_number  customer_number                   ,
           a.party_name customer_name                                               ,
           d.gl_date                                                                ,
           b.customer_trx_id                                                        ,
           b.trx_number                                                             ,
           (SELECT interface_line_Attribute1
           FROM ra_customer_Trx_lines_All
           where CUSTOMER_TRX_ID=b.CUSTOMER_TRX_ID
           and org_id=b.org_id
           and rownum=1)reference,
           to_char(b.trx_date,'DD-MM-YYYY') trx_date                                ,
           c.receipt_number                                                         ,
           to_char(c.receipt_date,'DD-MM-yyyy') receipt_date                        ,
           decode(e.amount_dr, null, 'CR','DR')   comments                          ,
           e.code_combination_id                                                    ,
           b.INVOICE_CURRENCY_CODE                                                  ,
           b.exchange_rate                                                          ,
           nvl(e.AMOUNT_DR, e.AMOUNT_CR)     amount                                 ,
           nvl(e.ACCTD_AMOUNT_DR,e.ACCTD_AMOUNT_CR)     acctd_amount                ,
           e.source_type                                                            ,
           xxcns_deb_led_get_narration(e.source_type,NULL,B.CUSTOMER_TRX_ID)naration,
           0 customer_trx_id                                                        ,
           0 customer_trx_line_id                                                   ,
           b.ROWID
           FROM
           hz_parties a, hz_cust_accounts hzca ,
           ra_customer_trx_all                                                     b,
           ar_cash_receipts_all                                                    c,
           ar_receivable_applications_all                                          d,
           ar_distributions_all                                                    e
           WHERE a.party_id = hzca.party_id
           AND hzca.cust_account_id                    =  b.BILL_TO_CUSTOMER_ID
           AND b.customer_trx_id                       =  d.APPLIED_CUSTOMER_TRX_ID
           AND c.cash_receipt_id                       =  d.cash_receipt_id
           AND e.SOURCE_ID                             =  d.receivable_application_id
           AND b.org_id                                = '{p_org_id}'
           AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
           AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
           AND   NVL(b.BILL_TO_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(b.BILL_TO_SITE_USE_ID,'99999999999999'))
           AND e.source_Type                           IN ('EXCH_LOSS', 'EXCH_GAIN')
           AND to_date(d.gl_date,'DD-MON-RRRR') BETWEEN to_date('{p_start_date}','DD-MON-RRRR')  AND to_date('{p_end_date}','DD-MON-RRRR')
           AND B.invoice_currency_code ='INR'
           UNION ALL
           -- Following Query for Exchange Gain and Loss for CM applied to the invoice
           SELECT
           hzca.cust_account_id customer_id ,
            B.BILL_TO_SITE_USE_ID customer_site_id                                        ,
           hzca.account_number  customer_number                   ,
           a.party_name customer_name                                               ,
           d.gl_date                                                                ,
           b.customer_trx_id                                                        ,
           b.trx_number                                                             ,
           (SELECT interface_line_Attribute1
           FROM ra_customer_Trx_lines_All
           where CUSTOMER_TRX_ID=b.CUSTOMER_TRX_ID
           and org_id=b.org_id
           and rownum=1)reference,
           to_char(b.trx_date,'DD-MM-YYYY') trx_date                                ,
           null                                                         ,
           null                      ,
           decode(e.amount_dr, null, 'CR','DR')   comments                          ,
           e.code_combination_id                                                    ,
           b.INVOICE_CURRENCY_CODE                                                  ,
           b.exchange_rate                                                          ,
           nvl(e.AMOUNT_DR, e.AMOUNT_CR)     amount                                 ,
           nvl(e.ACCTD_AMOUNT_DR,e.ACCTD_AMOUNT_CR)     acctd_amount                ,
           e.source_type                                                            ,
           xxcns_deb_led_get_narration(e.source_type,NULL,B.CUSTOMER_TRX_ID)naration,
           0 customer_trx_id                                                        ,
           0 customer_trx_line_id                                                   ,
           b.ROWID
           FROM
           hz_parties a, hz_cust_accounts hzca ,
           ra_customer_trx_all                                                     b,
           ar_payment_schedules_all                                               c,
           ar_receivable_applications_all                                          d,
           ar_distributions_all                                                    e
           WHERE a.party_id = hzca.party_id
           AND hzca.cust_account_id                    =  b.BILL_TO_CUSTOMER_ID
           AND b.customer_trx_id                       =  d.APPLIED_CUSTOMER_TRX_ID
           AND c.payment_schedule_id                       =  d.payment_schedule_id
           and c.class='CM'
           AND e.SOURCE_ID                             =  d.receivable_application_id
           AND b.org_id                                =   '{p_org_id}'
           AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
           AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
           AND   NVL(b.BILL_TO_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(b.BILL_TO_SITE_USE_ID,'99999999999999'))
           AND e.source_Type                           IN ('EXCH_LOSS', 'EXCH_GAIN')
           AND to_date(d.gl_date,'DD-MON-RRRR') BETWEEN to_date('{p_start_date}','DD-MON-RRRR')  AND to_date('{p_end_date}','DD-MON-RRRR')
           AND B.invoice_currency_code ='INR'
           ORDER BY 5,4
           '''
    cur_data = cursor_ora.execute(line_query)
    excel_write_data = cur_data.fetchall()
    print(excel_write_data, 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
    return HttpResponse('Done')

@api_view(['POST'])
def download_customer_ledger_passbook(request):
    '''
    Download the report from postgres database
    :param request:
    :return:
    '''
    data = request.data
    print(data,'daa========================')
    form_1_organisation = data['form_1-organisation']
    print(form_1_organisation,'JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ')
    res = form_1_organisation[4:]
    p_org_id = re.sub(r'\,.*', "", res)
    print(p_org_id,'----------------------')
    form_1_customer = data['form_1-customer']
    print(form_1_customer,'nnnnnnnnnnnnnnnnnnnnnnnnnnn')
    res1 = form_1_customer[4:]
    p_customer_id = re.sub(r'\ ,.*', "", res1)
    print(p_customer_id,'xxxxxeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    print(request.method,'sssssssssssssssssssss00000-----------------------------')

    P_CUSTOMER_SITE = data['form_1-customer_site']
    p_customer_type = data['form_1-customer_type']
    print(P_CUSTOMER_SITE,p_customer_type,'sssssssssssssssssssssssssss')
    start_date = data['s_date']
    end_date = data['e_date']
    p_end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime('%d-%b-%Y')
    p_start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime('%d-%b-%Y')
    print(p_start_date,p_end_date,'Date=============================================================')
    dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
    conn_ora = cx_Oracle.connect(user=r'apps', password='apps1234', dsn=dsn_tns)
    cursor_ora = conn_ora.cursor()
    print(conn_ora,'2222222222222222')
    # listdata = f'''
    #       select B.SITE_USE_ID,D.ADDRESS1||D.ADDRESS2||D.ADDRESS3||D.CITY
    # from HZ_CUST_ACCT_SITES_ALL A,HZ_CUST_SITE_USES_ALL B,HZ_PARTY_SITES
    # C,HZ_LOCATIONS D
    # WHERE A.CUST_ACCT_SITE_ID = B.CUST_ACCT_SITE_ID
    # AND C.LOCATION_ID=D.LOCATION_ID
    # AND C.PARTY_SITE_ID = A.PARTY_SITE_ID
    # AND b.SITE_USE_CODE='BILL_TO'
    # AND A.CUST_ACCOUNT_ID='{p_customer_id}'
    # AND A.ORG_ID ='{p_org_id}'
    #         '''
    # cur = cursor_ora.execute(listdata)
    # MRN_DATA = cur.fetchall()
    # print(MRN_DATA,'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc')
    # = 1041
    p_customer_id2= p_customer_id
    # p_end_date = '08-JUN-2020' 01-JUN-2019
    p_org_id = 105
    header_query=f'''select
        --distinct
         a.party_name customer_name, hzca.account_number customer_number,
         hzca.customer_class_code customer_type, b.bill_to_customer_id customer_id, b.invoice_currency_code curr_code,
         b.BILL_TO_SITE_USE_ID customer_site_id
        From
             hz_parties A, hz_cust_accounts hzca,
             ra_customer_trx_all B,
             ar_payment_schedules_all C --added on 13n
        Where a.party_id = hzca.party_id
        AND ( hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id))
           )
        AND 	NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
        AND   NVL(b.BILL_TO_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(b.BILL_TO_SITE_USE_ID,'99999999999999'))
        AND	b.bill_to_customer_id = hzca.cust_account_id
        AND 	to_date(b.trx_date,'DD-MON-RRRR') <= to_date('{p_end_date}','DD-MON-RRRR')
        AND 	b.complete_flag = 'Y'
        AND c.customer_trx_id = b.customer_trx_id --added on 13n
        AND       b.org_id='{p_org_id}'
        --group By a.customer_name, a.customer_number, --b.invoice_currency_code
        UNION
        Select
        --distinct
        a.party_name customer_name, hzca.account_number customer_number,
        hzca.customer_class_code customer_type, b.pay_from_customer customer_id, b.currency_code curr_code,
         D.CUSTOMER_SITE_USE_ID customer_site_id
        From
            hz_parties A, hz_cust_accounts hzca,
            ar_cash_receipts_all B,
          ar_cash_receipt_history_all C,
          ar_payment_schedules_all D --added on 13n
        Where a.party_id = hzca.party_id
        AND ( hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id))
             )
        AND NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
         AND  NVL(D.CUSTOMER_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(D.CUSTOMER_SITE_USE_ID,'99999999999999'))
        AND    b.pay_from_customer = hzca.cust_account_id
        AND    to_date(b.receipt_date,'DD-MON-RRRR')    <= to_date('{p_end_date}','DD-MON-RRRR') --Replaced gl_date with Receipt_date for bug#8459757 by JMEENA
        AND b.cash_receipt_id =c.cash_receipt_id
        AND d.cash_receipt_id = b.cash_receipt_id --added on 13n
        AND c.reversal_gl_date is null
        AND b.org_id='{p_org_id}'
        --group By a.customer_name, a.customer_number,
        --b.currency_code

        UNION
        Select
        --distinct
        a.party_name customer_name, hzca.account_number /*a.party_number*/ customer_number, /*Changes by nprashar for bug bug # 7256288*/
        hzca.customer_class_code customer_type,  b.pay_from_customer customer_id, b.currency_code curr_code ,
          C.CUSTOMER_SITE_USE_ID customer_site_id
        From
            hz_parties A, hz_cust_accounts hzca,
            ar_cash_receipts_all B,
        ar_payment_schedules_all C
        Where a.party_id = hzca.party_id
        AND  (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id )))
        AND       NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
        AND  NVL(C.CUSTOMER_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(C.CUSTOMER_SITE_USE_ID,'99999999999999'))
        AND    b.pay_from_customer = hzca.cust_account_id
        AND    to_date(b.reversal_date,'DD-MON-RRRR')      <= to_date('{p_end_date}','DD-MON-RRRR')
        AND c.cash_receipt_id =  b.cash_receipt_id --added on 13n
        AND       b.org_id='{p_org_id}'
        --group By a.customer_name, a.customer_number,
        --b.currency_code
        ----Query added for adjustment entries by sridhar on 14nov-00
        UNION
        SELECT
        A.party_name customer_name,
        hzca.account_number/*A.party_number*/ customer_number, /*Changes by nprashar for bug bug # 7256288*/
        hzca.customer_class_code customer_type,
        C.bill_to_customer_id customer_id,
        C.invoice_currency_code curr_code ,
         C.BILL_TO_SITE_USE_ID customer_site_id
        FROM
        hz_parties a, hz_cust_accounts hzca ,
        ar_adjustments_all b, ra_customer_trx_all c, ar_payment_schedules_all d
        WHERE     a.party_id = hzca.party_id
        AND    (  hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
        AND   NVL(C.BILL_TO_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(C.BILL_TO_SITE_USE_ID,'99999999999999'))
        AND       NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
        AND     b.customer_trx_id = c.customer_trx_id
        /*AND b.customer_trx_id not in (select customer_trx_id from ar_adjustments_all where CHARGEBACK_CUSTOMER_TRX_ID is not NULL or created_from = 'REVERSE_CHARGEBACK')*/ /*added by abezgam for bug#10228717*/
        /*Commented NOT IN and replaced with NOT EXISTS by mmurtuza for bug 14062515*/
        AND NOT EXISTS (
                  SELECT 'x'
                    FROM ar_adjustments_all
                   WHERE (   chargeback_customer_trx_id IS NOT NULL
                          OR created_from = 'REVERSE_CHARGEBACK'
                         )
                     AND customer_trx_id = b.customer_trx_id)
        AND     c.bill_to_customer_id = hzca.cust_account_id
        AND     to_date(b.apply_date,'DD-MON-RRRR') <= to_date('{p_end_date}','DD-MON-RRRR')
        AND     b.status = 'A'
        AND    b.customer_trx_id = d.customer_trx_id
        AND       c.org_id='{p_org_id}'
        ORDER BY 4
    '''
    cur = cursor_ora.execute(header_query)
    print(cur)
    customer_report = cur.fetchall()
    print(customer_report,' mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
    line_query = f'''Select
       hzca.cust_account_id  customer_id,
        B.BILL_TO_SITE_USE_ID customer_site_id,
       hzca.account_number customer_number   ,
       a.party_name   customer_name                             ,
       d.gl_date                                                ,
       B.CUSTOMER_TRX_ID                                        ,
       b.trx_number                                             ,
       (SELECT interface_line_Attribute1
       FROM ra_customer_Trx_lines_All
       where CUSTOMER_TRX_ID=b.CUSTOMER_TRX_ID
       and org_id=b.org_id
       and rownum=1)reference,
       TO_CHAR(b.trx_date, 'DD-MM-YYYY') trx_date               ,
       NULL receipt_number                                      ,
       NULL receipt_date                                        ,
       SUBSTR(b.comments,1,50) remarks                          ,
       d.code_combination_id account_id                         ,
       b.invoice_currency_code currency_code                    ,
       b.exchange_rate                                          ,
       d.amount amount                                          ,
       (d.amount * NVL(b.exchange_rate,1)) amount_other_currency,
       F.TYPE                                          ,
       xxcns_deb_led_get_narration(F.TYPE,F.NAME,B.CUSTOMER_TRX_ID)naration,
       b.customer_trx_id                                        ,
       d.customer_trx_line_id                                   ,
       b.rowid
       From
          hz_parties                                           a,
          hz_cust_accounts                                     hzca,
          ra_customer_trx_ALL                                  B,
          RA_CUST_TRX_LINE_GL_DIST_ALL                         D,
          GL_CODE_COMBINATIONS                                 E,
          RA_CUST_TRX_TYPES_ALL                                F,
          ar_payment_schedules_all                             G,
          hz_locations                                         loc,
          hz_party_sites                                       party_site,
          hz_cust_acct_sites_all                               acct_site,
          hz_cust_site_uses_all                                site
       Where a.party_id = hzca.party_id
       AND   b.bill_to_customer_id = hzca.cust_account_id
       AND      b.complete_flag       = 'Y'
       AND     d.customer_trx_id     = b.customer_trx_id
       AND     d.account_class       = 'REC'
       AND     e.code_combination_id = d.code_combination_id
       AND    f.cust_trx_type_id    = b.cust_trx_type_id
       AND     f.type in ('INV','CM','DM','DEP')
       AND     d.latest_rec_flag     = 'Y'
       AND     g.customer_trx_id     = b.customer_trx_id
       and   loc.location_id       = party_site.location_id
       and   party_site.party_site_id    = acct_site.party_site_id
       and   acct_site.cust_acct_site_id = site.cust_acct_site_id
       and   site.site_use_id            = g.customer_site_use_id
       AND     b.org_id              ='{p_org_id}'
       AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
       AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
       AND   NVL(b.BILL_TO_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(b.BILL_TO_SITE_USE_ID,'99999999999999'))
       AND      (g.gl_date) between  ('{p_start_date}')  AND ('{p_end_date}')
       AND b.invoice_currency_code='INR'
       and     g.payment_schedule_id in
       (select min(payment_schedule_id)
        from   ar_payment_schedules_all
        where  customer_trx_id = g.customer_trx_id)
       UNION
       -- Following Query for Cash receipts
       Select
       hzca.cust_account_id customer_id,
        F.CUSTOMER_SITE_USE_ID customer_site_id ,
       hzca.account_number  customer_number   ,
       a.party_name customer_name                               ,
       e.gl_date                                                ,
       0                                                        ,
       b.receipt_number                                                   ,
       NULL                                                     ,
       TO_CHAR(b.receipt_date,  'DD-MM-YYYY'),
       b.receipt_number                                        ,
       TO_CHAR(b.receipt_date,  'DD-MM-YYYY')                   ,
       NULL                                                     ,
       d.cash_ccid account_id                                   ,
       b.currency_code                                          ,
       b.exchange_rate                                          ,
       b.amount  amount                                         ,
       (b.amount * NVL(b.exchange_rate,1)) amount_other_currency,
       'REC' type                                               ,
       'Amount Received' naration,
       0                                                        ,
       0                                                        ,
       b.rowid
       From
           hz_parties a, hz_cust_accounts hzca,
           ar_cash_receipts_all                                B,
           gl_code_combinations                                C,
           ar_receipt_method_accounts_all                      D,
           ar_cash_receipt_history_all                         E,
                   ar_payment_schedules_all                            F
       Where a.party_id = hzca.party_id
       AND b.pay_from_customer                     = hzca.cust_account_id
       AND    b.remit_bank_acct_use_id            = d.remit_bank_acct_use_id
       AND         d.receipt_method_id                     = b.receipt_method_id
       AND    d.cash_ccid                             = c.code_combination_id
       AND         e.cash_receipt_id                       = b.cash_receipt_id
       AND E.cash_receipt_history_id in (SELECT    min(incrh.cash_receipt_history_id)
                                                     FROM    ar_cash_receipt_history_all incrh
                                                     WHERE   incrh.cash_receipt_id = B.cash_receipt_id
                                                     AND     incrh.status <> 'REVERSED' )
       AND     f.cash_receipt_id                           = b.cash_receipt_id
       AND     b.org_id                                   ='{p_org_id}'
       AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
       AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
       AND   NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999'))
       AND    (e.gl_date) between ('{p_start_date}')  AND ('{p_end_date}')
       AND b.currency_code ='INR'
       UNION
       -- Following Query for Receipt WriteOff
       Select
       hzca.cust_account_id customer_id  ,
        F.CUSTOMER_SITE_USE_ID customer_site_id                          ,
       hzca.account_number  customer_number,
       a.party_name customer_name ,
       g.gl_date     ,
       0                                                                ,
       b.receipt_number                                                             ,
       NULL ,
       TO_CHAR(b.receipt_date,  'DD-MM-YYYY'),
       b.receipt_number                                                 ,
       TO_CHAR(b.receipt_date,  'DD-MM-YYYY')                           ,
       NULL                                                             ,
       d.cash_ccid account_id                                           ,
       b.currency_code                                                  ,
       b.exchange_rate                                                  ,
       g.amount_applied  amount                                         ,
       (g.amount_applied * NVL(b.exchange_rate,1)) amount_other_currency,
       'W/O' type                                                       ,
       xxcns_deb_led_get_narration(TYPE,NULL,0)naration,
       0                                                                ,
       0                                                                ,
       b.rowid
       From
           hz_parties a, hz_cust_accounts hzca ,
           ar_cash_receipts_all                                        B,
           gl_code_combinations                                        C,
           ar_receipt_method_accounts_all                              D,
           ar_cash_receipt_history_all                                 E,
               ar_payment_schedules_all                                    F,
               ar_receivable_applications_all                              G
       Where a.party_id = hzca.party_id
       AND b.pay_from_customer                     = hzca.cust_account_id
       AND g.applied_payment_schedule_id           = -3
       AND g.cash_receipt_id                       = b.cash_receipt_id
       and g.cash_receipt_history_id               = e.cash_receipt_history_id
       AND g.status                                = 'ACTIVITY'
       AND    b.remit_bank_acct_use_id                = d.remit_bank_acct_use_id
       AND d.receipt_method_id                     = b.receipt_method_id
       AND    d.cash_ccid                             = c.code_combination_id
       AND e.cash_receipt_id                       = b.cash_receipt_id
       AND f.cash_receipt_id                       = b.cash_receipt_id
       AND b.org_id                                ='{p_org_id}'
       AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
       AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
       AND   NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999'))
       AND    (g.gl_date)  between ('{p_start_date}')  AND ('{p_end_date}')
       AND b.currency_code ='INR'
       and not exists
       (select 1
        from   ar_cash_receipt_history_all
        where  cash_receipt_id = b.cash_receipt_id
        and    status = 'REVERSED'
        )
       UNION
       -- Following Query for Receipt WriteOff
       Select
       hzca.cust_account_id customer_id  ,
        F.CUSTOMER_SITE_USE_ID customer_site_id                          ,
       hzca.account_number customer_number           ,
       a.party_name customer_name                                       ,
       g.gl_date     ,
       0                                                                ,
       b.receipt_number                                                            ,
       NULL ,
       TO_CHAR(b.receipt_date,  'DD-MM-YYYY')                                                       ,
       b.receipt_number                                                 ,
       TO_CHAR(b.receipt_date,  'DD-MM-YYYY')                           ,
       NULL                                                             ,
       d.cash_ccid account_id                                           ,
       b.currency_code                                                  ,
       b.exchange_rate                                                  ,
       g.amount_applied  amount                                         ,
       (g.amount_applied * NVL(b.exchange_rate,1)) amount_other_currency,
       'REF' type                                                       ,
       xxcns_deb_led_get_narration(TYPE,NULL,0)naration,
       0                                                                ,
       0                                                                ,
       b.rowid
       From
           hz_parties a, hz_cust_accounts hzca ,
           ar_cash_receipts_all                                        B,
           gl_code_combinations                                        C,
           ar_receipt_method_accounts_all                              D,
           ar_cash_receipt_history_all                                 E,
               ar_payment_schedules_all                                    F,
               ar_receivable_applications_all                              G
       Where a.party_id = hzca.party_id
       AND b.pay_from_customer                     = hzca.cust_account_id
       AND g.applied_payment_schedule_id           = -8
       AND g.cash_receipt_id                       = b.cash_receipt_id
       and g.cash_receipt_history_id               = e.cash_receipt_history_id
       AND g.status                                = 'ACTIVITY'
       AND    b.remit_bank_acct_use_id                = d.remit_bank_acct_use_id
       AND d.receipt_method_id                     = b.receipt_method_id
       AND    d.cash_ccid                             = c.code_combination_id
       AND e.cash_receipt_id                       = b.cash_receipt_id
       AND f.cash_receipt_id                       = b.cash_receipt_id
       AND b.org_id                                ='{p_org_id}'
       AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
       AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
       AND   NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999'))
       AND    (g.gl_date)  between ('{p_start_date}')  AND ('{p_end_date}')
       AND b.currency_code ='INR'
       and not exists
       (select 1
        from   ar_cash_receipt_history_all
        where  cash_receipt_id = b.cash_receipt_id
        and    status = 'REVERSED'
        )
       UNION
       -- Following Query for Receipt Reversal
       Select
       hzca.cust_account_id customer_id ,
        F.CUSTOMER_SITE_USE_ID customer_site_id,
       hzca.account_number customer_number           ,
       a.party_name customer_name                                       ,
       e.gl_date gl_date                                                ,
       0                                                                ,
       b.receipt_number ,
       NULL                                                             ,
       to_char(e.trx_date,'DD-MM-YYYY')  trx_date                       ,
       b.receipt_number                                                 ,
       TO_CHAR(b.receipt_date,  'DD-MM-YYYY')                           ,
       NULL                                                             ,
       c.code_combination_id account_id                                 ,
       b.currency_code                                                  ,
       b.exchange_rate                                                  ,
       b.amount amount                                                  ,
       (b.amount * NVL(b.exchange_rate,1)) amount_other_currency        ,
       'REV' type                                                       ,
       'Amount Reversed' naration,
       0                                                                ,
       0                                                                ,
       b.rowid
       From
           hz_parties a, hz_cust_accounts hzca ,
           ar_cash_receipts_all                                        B,
           gl_code_combinations                                        C,
           ar_receipt_method_accounts_all                              D,
           ar_cash_receipt_history_all                                 E,
               ar_payment_schedules_all                                    F
       Where a.party_id = hzca.party_id
       AND b.pay_from_customer                       = hzca.cust_account_id
       AND    b.remit_bank_acct_use_id                = d.remit_bank_acct_use_id
       AND d.receipt_method_id                     = b.receipt_method_id
       AND    d.cash_ccid                             = c.code_combination_id
       AND e.cash_receipt_id                       = b.cash_receipt_id
       AND f.cash_receipt_id                       = b.cash_receipt_id
       AND b.org_id                                = '{p_org_id}'
       AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
       AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
       AND   NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(F.CUSTOMER_SITE_USE_ID,'99999999999999'))
       AND e.status                                = 'REVERSED'
       AND    (e.gl_date) between ('{p_start_date}')  AND ('{p_end_date}')
       AND b.currency_code ='INR'
       and b.reversal_date is not null
       UNION
       -- Following Query for Adjustments
       SELECT
       HZCA.CUST_ACCOUNT_ID CUSTOMER_ID  ,
        C.BILL_TO_SITE_USE_ID customer_site_id                               ,
       hzca.account_number  CUSTOMER_NUMBER           ,
       A.PARTY_NAME CUSTOMER_NAME                                       ,
       B.GL_DATE                                                        ,
       0                                                                ,
       B.ADJUSTMENT_NUMBER                                              ,
       NULL,
       TO_CHAR(B.APPLY_DATE,'DD-MM-YYYY') trx_date                      ,
       NULL receipt_number                                              ,
       NULL receipt_date                                                ,
       SUBSTR(b.comments,1,50) remarks                                  ,
       b.code_combination_id account_id                                 ,
       c.invoice_currency_code currency_code                            ,
       c.exchange_rate                                                  ,
       b.amount amount                                                  ,
       (b.amount*NVL(c.exchange_rate,1)) amount_other_currency          ,
       'ADJ' type                                                       ,
       xxcns_deb_led_get_narration(TYPE,NULL,0)naration,
       0                                                                ,
       0                                                                ,
       b.rowid
       FROM
       HZ_PARTIES A, HZ_CUST_ACCOUNTS HZCA,
       ar_adjustments_all                                              b,
       ra_customer_trx_all                                             c,
       ar_payment_schedules_all                                        d,
       gl_code_combinations                                            e
       WHERE
            b.customer_trx_id                         = c.customer_trx_id
       AND a.party_id                              = hzca.party_id
       AND c.bill_to_customer_id                   = hzca.cust_account_id
       AND b.status                                = 'A'
       AND    e.code_combination_id                   = b.code_combination_id
       AND    b.payment_schedule_id                   = d.payment_schedule_id
       AND    b.customer_trx_id                       = d.customer_trx_id
       AND c.org_id                                ='{p_org_id}'
       AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
       AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
       AND   NVL(C.BILL_TO_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(C.BILL_TO_SITE_USE_ID,'99999999999999'))
       AND    (b.gl_date) between ('{p_start_date}')  AND ('{p_end_date}')
       AND c.invoice_currency_code ='INR'
       AND b.customer_trx_id not in (select customer_trx_id from ar_adjustments_all where CHARGEBACK_CUSTOMER_TRX_ID is not NULL or created_from = 'REVERSE_CHARGEBACK') /*added by abezgam for bug#10228717*/
       UNION ALL   ----comment by zakaul  UNION
       -- -- Following Query for Discounts
       Select
       hzca.cust_account_id customer_id,
        B.BILL_TO_SITE_USE_ID customer_site_id                                        ,
       hzca.account_number  customer_number                 ,
       a.party_name customer_name                                              ,
       d.gl_date                                                               ,
       B.CUSTOMER_TRX_ID                                                       ,
       b.trx_number                                                            ,
       (SELECT interface_line_Attribute1
       FROM ra_customer_Trx_lines_All
       where CUSTOMER_TRX_ID=b.CUSTOMER_TRX_ID
       and org_id=b.org_id
       and rownum=1)reference,
       TO_CHAR(b.trx_date, 'DD-MM-YYYY') trx_date                              ,
       NULL receipt_number                                                     ,
       NULL receipt_date                                                       ,
       SUBSTR(b.comments,1,50) remarks                                         ,
       earned_discount_ccid account_id                                                            ,
        b.invoice_currency_code currency_code                                  ,
       b.exchange_rate                                                         ,
       d.EARNED_discount_taken amount                                          ,
       d.ACCTD_EARNED_DISCOUNT_TAKEN  amount_other_currency ,
       'DSC' type                                                              ,
       'Cash Discount' naration,
       b.customer_trx_id                                                       ,
       0                                                                       ,
       b.rowid
       From
           hz_parties a, hz_cust_accounts hzca ,
           ra_customer_trx_all                                                B,
           ar_receivable_applications_all                                     D
       Where a.party_id = hzca.party_id
       AND b.bill_to_customer_id                   = hzca.cust_account_id
       AND    b.complete_flag                         = 'Y'
       AND D.EARNED_DISCOUNT_TAKEN                 is not null
       and D.EARNED_DISCOUNT_TAKEN                 <> 0
       AND b.org_id                                = '{p_org_id}'
       AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
       AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
       AND   NVL(b.BILL_TO_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(b.BILL_TO_SITE_USE_ID,'99999999999999'))
       and b.customer_trx_id                       = d.applied_customer_trx_id
       and d.application_type                      = 'CASH'
       and d.display                               = 'Y'
       AND (d.gl_date) between ('{p_start_date}')  AND ('{p_end_date}')
       AND B.invoice_currency_code ='INR'
       UNION ALL
       -- Following Query for Exchange Gain and Loss
       SELECT
       hzca.cust_account_id customer_id  ,
        B.BILL_TO_SITE_USE_ID customer_site_id                                       ,
       hzca.account_number  customer_number                   ,
       a.party_name customer_name                                               ,
       d.gl_date                                                                ,
       b.customer_trx_id                                                        ,
       b.trx_number                                                             ,
       (SELECT interface_line_Attribute1
       FROM ra_customer_Trx_lines_All
       where CUSTOMER_TRX_ID=b.CUSTOMER_TRX_ID
       and org_id=b.org_id
       and rownum=1)reference,
       to_char(b.trx_date,'DD-MM-YYYY') trx_date                                ,
       c.receipt_number                                                         ,
       to_char(c.receipt_date,'DD-MM-yyyy') receipt_date                        ,
       decode(e.amount_dr, null, 'CR','DR')   comments                          ,
       e.code_combination_id                                                    ,
       b.INVOICE_CURRENCY_CODE                                                  ,
       b.exchange_rate                                                          ,
       nvl(e.AMOUNT_DR, e.AMOUNT_CR)     amount                                 ,
       nvl(e.ACCTD_AMOUNT_DR,e.ACCTD_AMOUNT_CR)     acctd_amount                ,
       e.source_type                                                            ,
       xxcns_deb_led_get_narration(e.source_type,NULL,B.CUSTOMER_TRX_ID)naration,
       0 customer_trx_id                                                        ,
       0 customer_trx_line_id                                                   ,
       b.ROWID
       FROM
       hz_parties a, hz_cust_accounts hzca ,
       ra_customer_trx_all                                                     b,
       ar_cash_receipts_all                                                    c,
       ar_receivable_applications_all                                          d,
       ar_distributions_all                                                    e
       WHERE a.party_id = hzca.party_id
       AND hzca.cust_account_id                    =  b.BILL_TO_CUSTOMER_ID
       AND b.customer_trx_id                       =  d.APPLIED_CUSTOMER_TRX_ID
       AND c.cash_receipt_id                       =  d.cash_receipt_id
       AND e.SOURCE_ID                             =  d.receivable_application_id
       AND b.org_id                                = '{p_org_id}'
       AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
       AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
       AND   NVL(b.BILL_TO_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(b.BILL_TO_SITE_USE_ID,'99999999999999'))
       AND e.source_Type                           IN ('EXCH_LOSS', 'EXCH_GAIN')
       AND (d.gl_date) BETWEEN ('{p_start_date}')  AND ('{p_end_date}')
       AND B.invoice_currency_code ='INR'
       UNION ALL
       -- Following Query for Exchange Gain and Loss for CM applied to the invoice
       SELECT
       hzca.cust_account_id customer_id ,
        B.BILL_TO_SITE_USE_ID customer_site_id                                        ,
       hzca.account_number  customer_number                   ,
       a.party_name customer_name                                               ,
       d.gl_date                                                                ,
       b.customer_trx_id                                                        ,
       b.trx_number                                                             ,
       (SELECT interface_line_Attribute1
       FROM ra_customer_Trx_lines_All
       where CUSTOMER_TRX_ID=b.CUSTOMER_TRX_ID
       and org_id=b.org_id
       and rownum=1)reference,
       to_char(b.trx_date,'DD-MM-YYYY') trx_date                                ,
       null                                                         ,
       null                      ,
       decode(e.amount_dr, null, 'CR','DR')   comments                          ,
       e.code_combination_id                                                    ,
       b.INVOICE_CURRENCY_CODE                                                  ,
       b.exchange_rate                                                          ,
       nvl(e.AMOUNT_DR, e.AMOUNT_CR)     amount                                 ,
       nvl(e.ACCTD_AMOUNT_DR,e.ACCTD_AMOUNT_CR)     acctd_amount                ,
       e.source_type                                                            ,
       xxcns_deb_led_get_narration(e.source_type,NULL,B.CUSTOMER_TRX_ID)naration,
       0 customer_trx_id                                                        ,
       0 customer_trx_line_id                                                   ,
       b.ROWID
       FROM
       hz_parties a, hz_cust_accounts hzca ,
       ra_customer_trx_all                                                     b,
       ar_payment_schedules_all                                               c,
       ar_receivable_applications_all                                          d,
       ar_distributions_all                                                    e
       WHERE a.party_id = hzca.party_id
       AND hzca.cust_account_id                    =  b.BILL_TO_CUSTOMER_ID
       AND b.customer_trx_id                       =  d.APPLIED_CUSTOMER_TRX_ID
       AND c.payment_schedule_id                       =  d.payment_schedule_id
       and c.class='CM'
       AND e.SOURCE_ID                             =  d.receivable_application_id
       AND b.org_id                                =   '{p_org_id}'
       AND (hzca.cust_account_id = NVL('{p_customer_id}',NVL('{p_customer_id2}', hzca.cust_account_id)))
       AND   NVL(hzca.customer_class_code,' ') = NVL('{p_customer_type}', NVL(hzca.customer_class_code,' '))
       AND   NVL(b.BILL_TO_SITE_USE_ID,'99999999999999') = NVL('{P_CUSTOMER_SITE}',NVL(b.BILL_TO_SITE_USE_ID,'99999999999999'))
       AND e.source_Type                           IN ('EXCH_LOSS', 'EXCH_GAIN')
       AND (d.gl_date) BETWEEN ('{p_start_date}')  AND ('{p_end_date}')
       AND B.invoice_currency_code ='INR'
       ORDER BY 5,4
       '''
    cur_data = cursor_ora.execute(line_query)
    excel_write_data = cur_data.fetchall()
    print(excel_write_data, 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
    output = BytesIO()
    print(output, 'ffffffffffffffffffffffffffffffffff')
    for header in customer_report:
        name = header[0]
        print(name,'llllllllllllllllllll')
        id = header[3]
        customer_no = header[1]
        customer_type_ =header[2]
        currency_code = header[4]
        customer_site_id = header[5]
        # customer_details = "Id :"+ str(id)+", "+"Name :" + name + ", " + "C No :"+customer_no

        workbook = xlsxwriter.Workbook(output)
        # workbook = xlsxwriter.Workbook('demo1.xlsx')
        worksheet1 = workbook.add_worksheet()
        row_count = 17
        column_count = 1
        caption = 'Passbook'

        # Some sample data for the table.
        data = [
            ['Organization Deatils', form_1_organisation],
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
        bold = workbook.add_format({'bold': True})
        worksheet1.write('B1', caption, bold)

        # Add a table to the worksheet.
        worksheet1.add_table('B2:C11', {'data': data or None})

        worksheet1.write('B13', 'RUNTOT', bold)
        worksheet1.write('D15', 'Opening Balance', bold)
        worksheet1.write('E15', 'OP_TOT_DR', bold)
        worksheet1.write('F15', 'OP_TOT_CR', bold)

        table_row_count = row_count + (len(excel_write_data) or 1)
        print(table_row_count, 'wwwwwww')
        #
        table_headers = worksheet1.add_table(row_count, column_count,
             table_row_count, 7, {'data': excel_write_data,
                                        'columns': [{'header': 'Document No.'},
                                                    {'header': 'Document Date'},
                                                    {'header': 'Document Type'},
                                                    {'header': 'Reference'},
                                                    {'header': 'Debit'},
                                                    {'header': 'Credit'},
                                                    {'header': 'Running Balance'},

                                                    ]})

        worksheet1.add_table('K19:M21', {
                'columns': [{'header': 'Closing Balance'},
                            {'header': 'CF_CLOSING_TOT'},
                            {'header': 'CF_CLOSING_TOTCR'},
                            ]})
        workbook.close()
        output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    return response
