from string import ascii_uppercase
from django.views.generic import TemplateView
import cx_Oracle
from django_popup_view_field.registry import registry_popup_view


class OrganisationIdPopupView(TemplateView):
    template_name = "popups/popup_organisation_data.html"
    item = None

    def get(self, request, *args, **kwargs):
        ou_id_val = []
        ou_name_val =[]
        if "code" in request.GET or "itemcode" in request.GET:
            itemcode = request.GET.get('itemcode')
            code = request.GET.get('code')
            dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
            connection_oracle = cx_Oracle.connect(user=r'apps', password='apps1234', dsn=dsn_tns, encoding="UTF-8")
            cursor_conn = connection_oracle.cursor()
            listdata = f'''
           select distinct ou_id,ou_name
  from apps.xxcns_org where ou_name LIKE '%{itemcode}%' OR ou_name LIKE '%{code}%'
            '''
            cur = cursor_conn.execute(listdata)
            MRN_DATA = cur.fetchall()

            for j in MRN_DATA:
                ou_id_val.append(j[0])
                ou_name_val.append(j[1])
        request.session['ou_id'] = ou_id_val
        list_val = zip(ou_id_val,ou_name_val)
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
        if "code" in request.GET or "itemcode" in request.GET:
            party_name = request.GET.get('itemcode')
            code = request.GET.get('code')
            dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
            connection_oracle = cx_Oracle.connect(user=r'apps', password='apps1234', dsn=dsn_tns, encoding="UTF-8")
            cursor_conn = connection_oracle.cursor()
            listdata = f'''
           SELECT hzca.account_number customer_no, party_name customer_name,
        hzca.cust_account_id customer_id
   FROM hz_parties hzp, hz_cust_accounts_all hzca
  WHERE hzp.party_id = hzca.party_id AND (party_name LIKE '{party_name}%' OR party_name LIKE '{code}%')
--'M. B. AUTOMATION'
            '''
            cur = cursor_conn.execute(listdata)
            MRN_DATA = cur.fetchall()
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
        customer_id_ = request.session.get('customer_id_')
        ou_id = request.session.get('ou_id')
        # itemcode = request.GET.get('itemcode')
        # code = request.GET.get('code')
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
AND A.CUST_ACCOUNT_ID='{customer_id_}'
AND A.ORG_ID ='{ou_id}'
        '''
        cur = cursor_conn.execute(listdata)
        MRN_DATA = cur.fetchall()
        for j in MRN_DATA:
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

# print(main_list_val,'ooooooooooooooooooooooooooooooooooo')
registry_popup_view.register(OrganisationIdPopupView)
registry_popup_view.register(CustomerSitePopupView)
registry_popup_view.register(CustomerPopupView)

