from string import ascii_uppercase
from django.views.generic import TemplateView
import cx_Oracle
from django_popup_view_field.registry import registry_popup_view
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from .models import UserForm
from django.db import connection
print(UserForm,'dddddddddddd')
@api_view(['POST'])
def customer_data(request):
    '''
    Download the report from postgres database
    :param request:
    :return:
    '''
    data = request.data
    default11 =data['default11']
    request.session['default11'] = default11
    return HttpResponse('Done')


class OrganisationIdPopupView(TemplateView):
    template_name = "popups/popup_organisation_data.html"
    item = None
    customer =None

    def get(self, request, *args, **kwargs):
        ou_id_val = []
        ou_name_val = []

        if "code" in request.GET or "org_val" in request.GET:
            org_val = request.GET.get('org_val')
            code = request.GET.get('code')
            dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
            connection_oracle = cx_Oracle.connect(user=r'apps', password='apps1234', dsn=dsn_tns, encoding="UTF-8")
            cursor_conn = connection_oracle.cursor()
            listdata = f'''
             select distinct ou_id,ou_name
    from apps.xxcns_org where ou_name LIKE '%{org_val}%' OR ou_name LIKE '%{code}%' 
              '''
            cur = cursor_conn.execute(listdata)
            MRN_DATA = cur.fetchall()

            for j in MRN_DATA:
                ou_id_val.append(j[0])
                ou_name_val.append(j[1])
        list_val = zip(ou_id_val, ou_name_val)
        qs = list_val
        self.item = qs

        return super(OrganisationIdPopupView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrganisationIdPopupView, self).get_context_data(**kwargs)

        context['item'] = self.item
        context['ascii_uppercase'] = ascii_uppercase
        # context['list_val'] = list_val
        return context


main_list_val= []
class CustomerPopupView(TemplateView):
    template_name = "popups/popup_customer_data.html"

    item = None

    def get(self, request, *args, **kwargs):
        customer_no_val = []
        customer_name_val =[]
        customer_id_val= []
        user_id = None
        if request.user.is_authenticated:
            print(request.user.is_authenticated,'sssssssssssssssssssssssssss')
            user_id = request.user.id
            print(user_id,'ddddddddd33333333333333333333333333333')
            cursor = connection.cursor()
            check_user_branch = f'''
                        SELECT branch FROM public.app_userform where user_id = '{user_id}'
                        '''
            cursor.execute(check_user_branch)
            branch_details = cursor.fetchall()
            customer_branch = str(branch_details).replace('[','').replace(',)]',')').replace(",","','")
            print(customer_branch,'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
            if "code" in request.GET or "itemcode" in request.GET:
                branch_name='Delhi'
                party_name = request.GET.get('itemcode')
                code = request.GET.get('code')
                dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
                connection_oracle = cx_Oracle.connect(user=r'apps', password='apps1234', dsn=dsn_tns, encoding="UTF-8")
                cursor_conn = connection_oracle.cursor()
                listdata = f'''
                select DISTINCT 
                ac.customer_number ,ac.customer_name ,
                hcas.cust_account_id customer_id,SEGMENT4 BRANCH
                from hz_cust_acct_Sites_All hcas,ra_territories rt,ar_customers ac
                where hcas.TERRITORY_ID=rt.TERRITORY_ID
                and ac.customer_id= hcas.cust_account_id
                and (customer_name LIKE '%{party_name}%' OR customer_name LIKE '%{code}%')
                and SEGMENT4  IN {customer_branch}
--('Delhi','Mumbai')
                '''
                cur = cursor_conn.execute(listdata)
                MRN_DATA = cur.fetchall()
                print(MRN_DATA,'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
                for j in MRN_DATA:
                    customer_no_val.append(j[0])
                    customer_id_val.append(j[2])

                    customer_name_val.append(j[1])

        # main_list_val.append(customer_id_val)
        request.session['customer_id_'] = customer_id_val
        list_val = zip(customer_id_val,customer_name_val, customer_no_val)
        qs = list_val
        self.item = qs
        return super(CustomerPopupView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CustomerPopupView, self).get_context_data(**kwargs)
        context['item'] = self.item
        context['ascii_uppercase'] = ascii_uppercase
        # context['list_val'] = list_val
        return context


class CustomerSitePopupView(TemplateView):
    template_name = "popups/popup_customer_site_data.html"
    item = None

    def get(self, request, *args, **kwargs):
        ou_id_val = []
        ou_name_val =[]
        list_val =[]
        p_cus_id = request.session.get('p_cus_id')
        p_org_id = request.session.get('p_org_id')
        dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
        connection_oracle = cx_Oracle.connect(user=r'apps', password='apps1234', dsn=dsn_tns, encoding="UTF-8")
        cursor_conn = connection_oracle.cursor()
        listdata = f'''
            select B.SITE_USE_ID,D.ADDRESS1||D.ADDRESS2||D.ADDRESS3||D.CITY
            from HZ_CUST_ACCT_SITES_ALL A,HZ_CUST_SITE_USES_ALL B,HZ_PARTY_SITES
            C,HZ_LOCATIONS D
            WHERE A.CUST_ACCT_SITE_ID = B.CUST_ACCT_SITE_ID
            AND C.LOCATION_ID=D.LOCATION_ID
            AND C.PARTY_SITE_ID = A.PARTY_SITE_ID
            AND b.SITE_USE_CODE='BILL_TO'
            AND A.CUST_ACCOUNT_ID='{p_cus_id}'
            AND A.ORG_ID ='{p_org_id}'
        '''
        cur = cursor_conn.execute(listdata)
        custoer_site_data = cur.fetchall()
        for j in custoer_site_data:
            ou_id_val.append(j[0])
            ou_name_val.append(j[1])
        list_val = zip(ou_id_val,ou_name_val)
        qs = list_val
        self.item = qs
        return super(CustomerSitePopupView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CustomerSitePopupView, self).get_context_data(**kwargs)

        context['item'] = self.item
        context['ascii_uppercase'] = ascii_uppercase
        # context['list_val'] = list_val
        return context

registry_popup_view.register(OrganisationIdPopupView)
registry_popup_view.register(CustomerSitePopupView)
registry_popup_view.register(CustomerPopupView)

