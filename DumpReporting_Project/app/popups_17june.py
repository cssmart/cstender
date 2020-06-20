from string import ascii_uppercase
from django.views.generic import TemplateView
import cx_Oracle
from django_popup_view_field.registry import registry_popup_view
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse

@api_view(['POST'])
def customer_data(request):
    '''
    Download the report from postgres database
    :param request:
    :return:
    '''
    data = request.data
    default11 =data['default11']
    print(default11,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    request.session['default11'] = default11
    print(request.session['default11'],'request.session  -kkkkkkkkkkkkkkkkkkkk-------------------------------------')
    return HttpResponse('Done')


class OrganisationIdPopupView(TemplateView):
    template_name = "popups/popup_organisation_data.html"
    item = None
    customer =None

    def get(self, request, *args, **kwargs):
        default11 = request.session.get('default11')
        print(default11, 'ccccccccccccccccccccccccccwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
        ou_id_val = []
        ou_name_val =[]
        customer_no_val = []
        customer_name_val =[]
        customer_id_val= []
        search = request.GET.get('search')
        print(search, 'cccccccccccccccccccce22222')
        #cs01
        f =open('organisation.txt','w')
        f.write(str(search))
        f.close()
        customer_search = request.GET.get('customer_search')
        print(customer_search, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        #Chopra, cs01
        f =open('cutomer.txt','w')
        f.write(str(search))
        f.close()
        if "search" in request.GET:
            print('ffffffffffffffffffffffffffffffffff')

            code = request.GET.get('code')
            dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
            connection_oracle = cx_Oracle.connect(user=r'apps', password='apps1234', dsn=dsn_tns, encoding="UTF-8")
            cursor_conn = connection_oracle.cursor()
            print(cursor_conn,'cccccccccccccccccccccccccccccccccccccccccppppppppppppppppppppppppppppp')
            listdata = f'''
                    select distinct ou_id,ou_name
                    from apps.xxcns_org where ou_name LIKE '%{search}%'
            '''
            cur = cursor_conn.execute(listdata)
            MRN_DATA = cur.fetchall()
            print(MRN_DATA,'cccccccccccccccccccccccccccc')

            for j in MRN_DATA:
                ou_id_val.append(j[0])
                ou_name_val.append(j[1])
            search = request.GET.get('search')
            print(search,'vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')

        elif "customer_search" in request.GET:
            code = request.GET.get('code')
            dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
            connection_oracle = cx_Oracle.connect(user=r'apps', password='apps1234', dsn=dsn_tns, encoding="UTF-8")
            cursor_conn = connection_oracle.cursor()
            print(cursor_conn,'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
            print(request.method,'xxxxxswwwwww')
            print(request.POST,'ddddddd222222222')
            search1 = request.POST.get('search')
            print(search1, 'xxxxxxxxxxwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww2222222222222222222222222222222222222222222')
            listdata = f'''
                                         select distinct ou_id,ou_name
                                         from apps.xxcns_org where ou_name LIKE '%{search1}%'
                                 '''
            cur = cursor_conn.execute(listdata)
            org_data = cur.fetchall()
            print(org_data, 'ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
            listdata = f'''
                       SELECT hzca.account_number customer_no, party_name customer_name,
                    hzca.cust_account_id customer_id
               FROM hz_parties hzp, hz_cust_accounts_all hzca
              WHERE hzp.party_id = hzca.party_id AND (party_name LIKE '{customer_search}%')
            --'M. B. AUTOMATION'
                        '''
            cur = cursor_conn.execute(listdata)
            customer_data = cur.fetchall()
            print(customer_data,'customer_data====888888888888888888888888888=====================')

            for j in customer_data:
                customer_no_val.append(j[0])
                customer_id_val.append(j[2])

                customer_name_val.append(j[1])
            search = request.GET.get('search')
            print(search, 'search------------------------------------>')

        elif 'cust_site' in request.GET:
            print('dddddddddd3333333333333333333333333333333333333333333333333')

        if "search" in request.GET:
            list_values = zip(ou_id_val, ou_name_val)
            print(list_values,'ccccccccccccccccccccccccccccccccccccccccccccccccccc')
            qs = list_values
            self.item = qs
        elif "customer_search" in request.GET:
            list_val = zip(customer_id_val, customer_name_val, customer_no_val)
            print(list_val, 'dddddddddddddddddd=======================')
            qs1 = list_val
            self.customer = qs1



        return super(OrganisationIdPopupView, self).get(request, *args, **kwargs)

    def post(self, request,*args, **kwargs):
        data = request.data
        default11 = data['default11']
        print(data,'search=================================================')


    def get_context_data(self, **kwargs):
        context = super(OrganisationIdPopupView, self).get_context_data(**kwargs)
        search = self.request.GET.get("search")
        extra_param = self.request.GET.get("extra_param")
        my_pk = self.request.GET.get("my_pk")
        print(extra_param,my_pk,'ppppppppppppppppppppppppppp')
        print(search, 'lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll')
        context['item'] = self.item
        print(context['item'],'cccccccccccccccccccccccccccccccccc')
        context['customer'] = self.customer
        print(context['customer'],'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        context['ascii_uppercase'] = ascii_uppercase
        # context['list_val'] = list_val
        return context


main_list_val= []
class CustomerPopupView(TemplateView):
    template_name = "popups/popup_customer_data.html"

    item = None

    def get(self, request, *args, **kwargs):
        print(request.GET.get('extra_param'),'dddddddddddddddddddddddddd')  # --> will be "Foo Bar"
        print(request.GET.get('my_pk'),'ooooooooooooooooooooooooooooooooooooooo')
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
        itemcode = self.request.GET.get("itemcode")
        print(itemcode,'ccccccccccccccccccceeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')

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
        if "org_id" in request.GET or "customer_id" in request.GET:
            org_id = request.GET.get('org_id')
            customer_id = request.GET.get('customer_id')
            print(customer_id,org_id,'lllllllllllllllllllllllllllllllllll')
            dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
            connection_oracle = cx_Oracle.connect(user=r'apps', password='apps1234', dsn=dsn_tns, encoding="UTF-8")
            cursor_conn = connection_oracle.cursor()
            print('Connection Stablish===', cursor_conn)
            listdata = f'''
                select B.SITE_USE_ID,D.ADDRESS1||D.ADDRESS2||D.ADDRESS3||D.CITY
                from HZ_CUST_ACCT_SITES_ALL A,HZ_CUST_SITE_USES_ALL B,HZ_PARTY_SITES
                C,HZ_LOCATIONS D
                WHERE A.CUST_ACCT_SITE_ID = B.CUST_ACCT_SITE_ID
                AND C.LOCATION_ID=D.LOCATION_ID
                AND C.PARTY_SITE_ID = A.PARTY_SITE_ID
                AND b.SITE_USE_CODE='BILL_TO'
                AND A.CUST_ACCOUNT_ID='{customer_id}'
                AND A.ORG_ID ='{org_id}'
            '''
            cur = cursor_conn.execute(listdata)
            custoer_site_data = cur.fetchall()
            print(custoer_site_data,'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
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

# print(main_list_val,'ooooooooooooooooooooooooooooooooooo')
registry_popup_view.register(OrganisationIdPopupView)
registry_popup_view.register(CustomerSitePopupView)
registry_popup_view.register(CustomerPopupView)

