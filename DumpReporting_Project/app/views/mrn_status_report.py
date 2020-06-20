from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import xlsxwriter
import cx_Oracle
from io import BytesIO, StringIO
from app.forms import MRNReportForm, MRNReportDownloadForm
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import psycopg2
from django.contrib import messages
TABLE_REPORT_NAME = "public.dump_table_report"
from django.db import connection
from datetime import datetime
from app.db import oracle_db_connection

TABLE_NAME='MRN_NEW_REPORT'
REPLACE_TABLE_NAME='MRN_Report3'

table_create =f""" CREATE TABLE {TABLE_NAME} (ge_number VARCHAR(300),
ge_date VARCHAR(300),
ORGANIZATION_ID VARCHAR(300),
orgname VARCHAR(300),
ATTRIBUTE7 VARCHAR(300),
SHIPMENT_HEADER_ID VARCHAR(300),
transaction_id VARCHAR(300),
SHIPMENT_LINE_ID VARCHAR(300),
RECEIPT_NUM VARCHAR(300),
CREATION_DATE VARCHAR(300),
VENDOR_NAME VARCHAR(300),
ATTRIBUTE1 VARCHAR(300),
ATTRIBUTE2 VARCHAR(300))"""
from django.contrib.auth.decorators import permission_required


# @permission_required('app.view_mrn_report')
def mrn_status_report_parameter(request):
    '''
    Create front view to access the data from the oracle DB..
    :param request:
    :return:
    '''
    form = MRNReportForm(request.POST or None)
    if form.is_valid():
        data = form.save(commit=False)
        form.save()
        return redirect('.')
    else:
        print(form.errors)
    return render(request, 'app/app/mrn_report_parameter_status.html', {'form': form})


@api_view(['POST'])
def mrn_status_report_view(request):
    data = request.data
    inventory_org = data['inventory_org']
    table_type = data['table_type']
    item_category = data['item_category']
    from_date = data['from_date']
    to_date = data['to_date']
    vender = data['vender']
    po_number = data['po_number']
    mrn_no = data['mrn_no']
    gate_entry_no =data['gate_entry_no']
    status = data['status']
    dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
    conn_ora = cx_Oracle.connect(user=r'apps', password='apps1234', dsn=dsn_tns)
    cursor_ora = conn_ora.cursor()

    list_data=f"""select distinct A.* from (SELECT DISTINCT
                    c.ATTRIBUTE6||'","'||
                    c.attribute8||'","'||
                    B.ORGANIZATION_ID||'","'||
                    (select organization_name from org_organization_definitions where organization_id = b.organization_id)||'","'||
                    c.ATTRIBUTE7||'","'||
                    B.SHIPMENT_HEADER_ID||'","'||
                    B.transaction_id||'","'||
                    rsl.SHIPMENT_LINE_ID||'","'||
                    C.RECEIPT_NUM||'","'||
                    TRUNC(B.TRANSACTION_DATE)||'","'||
                    pv.VENDOR_NAME||'","'||
                    C.ATTRIBUTE1||'","'||
                    C.ATTRIBUTE2
                    from 
                    PO_HEADERS_all A,
                    PO_LINES_ALL PLA,
                    RCV_TRANSACTIONS B,
                    RCV_SHIPMENT_HEADERS C,
                    rcv_shipment_lines rsl,
                    po_vendors pv,
                    po_vendor_sites_all pvs,
                    HR_ORGANIZATION_UNITS_V  hou
                    WHERE 1=1
                    and c.ship_to_org_id = hou.organization_id
                    and A.PO_HEADER_ID=B.PO_HEADER_ID
                    AND A.PO_HEADER_ID = PLA.PO_HEADER_ID
                    AND PLA.LINE_TYPE_ID = '3' 
                    AND B.SHIPMENT_HEADER_ID=C.SHIPMENT_HEADER_ID
                    AND B.TRANSACTION_TYPE='RECEIVE'
                    and b.VENDOR_ID=c.VENDOR_ID
                    and c.VENDOR_ID=pv.VENDOR_ID
                    and pv.VENDOR_ID=pvs.VENDOR_ID
                    and a.VENDOR_SITE_ID=pvs.VENDOR_SITE_ID
                    AND B.SHIPMENT_HEADER_ID=C.SHIPMENT_HEADER_ID-----
                    and B.SHIPMENT_LINE_ID = rsl.SHIPMENT_LINE_ID-----
                    and b.ORGANIZATION_ID = '{inventory_org}'
                    and c.ship_to_org_id = '{inventory_org}'
                    AND C.SHIPMENT_HEADER_ID= NVL('{mrn_no}',C.SHIPMENT_HEADER_ID)
                    AND B.TRANSACTION_DATE>= '{from_date}'
                    AND B.TRANSACTION_DATE<tO_DATE('{to_date}')+1
                    AND pv.vendor_id = nvl('{vender}',pv.vendor_id)
                    and A.po_header_id = nvl('{po_number}',A.po_header_id)
                    and nvl(c.attribute6,'aaa') = nvl('{gate_entry_no}',nvl(c.attribute6,'aaa'))
                    AND ('{item_category}' = 'Jobwork' OR NVL('{item_category}','All') = 'All')
                    UNION ALL
                    SELECT DISTINCT
                    c.ATTRIBUTE6||'","'||
                    c.attribute8||'","'||
                    B.ORGANIZATION_ID||'","'||
                    (select organization_name from org_organization_definitions where organization_id = b.organization_id)||'","'||
                    c.ATTRIBUTE7||'","'||
                    B.SHIPMENT_HEADER_ID||'","'||
                    B.transaction_id||'","'||
                    rsl.SHIPMENT_LINE_ID||'","'||
                    C.RECEIPT_NUM||'","'||
                    TRUNC(B.TRANSACTION_DATE)||'","'||
                    pv.VENDOR_NAME||'","'||
                    C.ATTRIBUTE1||'","'||
                    C.ATTRIBUTE2
                    from 
                    PO_HEADERS_all A,
                    PO_LINES_ALL PLA,
                    RCV_TRANSACTIONS B,
                    RCV_SHIPMENT_HEADERS C,
                    rcv_shipment_lines rsl,
                    po_vendors pv,
                    po_vendor_sites_all pvs,
                    HR_ORGANIZATION_UNITS_V  hou
                    WHERE 1=1
                    and c.ship_to_org_id = hou.organization_id
                    and A.PO_HEADER_ID=B.PO_HEADER_ID 
                    AND A.PO_HEADER_ID = PLA.PO_HEADER_ID
                    AND PLA.LINE_TYPE_ID <> '3'
                    AND B.SHIPMENT_HEADER_ID=C.SHIPMENT_HEADER_ID
                    AND B.TRANSACTION_TYPE='RECEIVE'
                    and b.VENDOR_ID=c.VENDOR_ID
                    and c.VENDOR_ID=pv.VENDOR_ID
                    and pv.VENDOR_ID=pvs.VENDOR_ID
                    and a.VENDOR_SITE_ID=pvs.VENDOR_SITE_ID
                    AND B.SHIPMENT_HEADER_ID=C.SHIPMENT_HEADER_ID-----
                    and B.SHIPMENT_LINE_ID = rsl.SHIPMENT_LINE_ID-----
                    and b.ORGANIZATION_ID = '{inventory_org}'
                    and c.ship_to_org_id = '{inventory_org}'
                    AND C.SHIPMENT_HEADER_ID= NVL('{mrn_no}',C.SHIPMENT_HEADER_ID)
                    AND B.TRANSACTION_DATE>= '{from_date}' 
                    AND B.TRANSACTION_DATE<  tO_DATE('{to_date}')+1
                    AND pv.vendor_id = nvl('{vender}',pv.vendor_id)
                    and A.po_header_id = nvl('{po_number}',A.po_header_id)
                    and nvl(c.attribute6,'aaa') = nvl('{gate_entry_no}',nvl(c.attribute6,'aaa'))
                    AND ('{item_category}' = 'Purchase' OR NVL('{item_category}','All') = 'All')
                    union all
                    SELECT DISTINCT c.ATTRIBUTE6||'","'||
                    c.attribute8||'","'||
                    B.ORGANIZATION_ID||'","'||
                    (select organization_name from org_organization_definitions where organization_id = b.organization_id)||'","'||
                    c.ATTRIBUTE7||'","'||
                    B.SHIPMENT_HEADER_ID||'","'||
                    B.transaction_id||'","'||
                    rsl.SHIPMENT_LINE_ID||'","'||
                    C.RECEIPT_NUM||'","'||
                    B.TRANSACTION_DATE||'","'||
                    ac.customer_NAME||'","'||
                    C.ATTRIBUTE1||'","'||
                    C.ATTRIBUTE2
                    from 
                       RCV_TRANSACTIONS B,
                       RCV_Shipment_HEADERS C,
                       rcv_shipment_lines rsl,
                    ar_customers ac,
                    HZ_CUST_ACCOUNTS HCA,
                    HZ_CUST_ACCT_SITES_ALL HCS,
                    hz_cust_site_uses_all hcsu,
                    HR_ORGANIZATION_UNITS_V  hou,
                    HZ_LOCATIONS HZL,
                    hz_party_sites hps
                    WHERE 1=1
                    AND B.SHIPMENT_HEADER_ID=C.SHIPMENT_HEADER_ID
                    AND C.SHIP_TO_ORG_ID = HOU.ORGANIZATION_ID
                    AND C.SHIP_TO_ORG_ID = '{inventory_org}'
                    AND B.TRANSACTION_TYPE='RECEIVE'
                    and c.customer_ID=ac.customer_ID
                    and ac.CUSTOMER_ID= HCA.CUST_ACCOUNT_ID
                    AND HCA.CUST_ACCOUNT_ID = HCS.CUST_ACCOUNT_ID
                    AND HCS.PARTY_SITE_ID = HPS.PARTY_SITE_ID
                    and hca.party_id=hps.party_id
                    and hcs.CUST_ACCT_SITE_ID=hcsu.CUST_ACCT_SITE_ID
                    and hcsu.SITE_USE_CODE='BILL_TO'
                    AND B.SHIPMENT_HEADER_ID=C.SHIPMENT_HEADER_ID-----
                    and B.SHIPMENT_LINE_ID = rsl.SHIPMENT_LINE_ID-----
                    and b.ORGANIZATION_ID = '{inventory_org}'
                    AND B.ORGANIZATION_ID=hcs.ORG_ID
                    AND C.SHIPMENT_HEADER_ID= NVL('{mrn_no}',C.SHIPMENT_HEADER_ID)
                    AND hps.location_id = hzl.location_id
                    AND B.TRANSACTION_DATE>='{from_date}'							 
                    AND B.TRANSACTION_DATE<tO_DATE('{to_date}')+1
                    and  ac.customer_id = nvl('{vender}',ac.customer_id)
                    and  nvl(c.attribute6,'aaa') = nvl('{gate_entry_no}', nvl(c.attribute6,'aaa'))
                    AND ('{item_category}' = 'RMA' OR NVL('{item_category}','All') = 'All')
                    union all
                    SELECT DISTINCT c.ATTRIBUTE6||'","'||
                    c.attribute8||'","'||
                    B.ORGANIZATION_ID||'","'||
                    (select organization_name from org_organization_definitions where organization_id = b.organization_id)||'","'||
                    c.ATTRIBUTE7||'","'||
                    B.SHIPMENT_HEADER_ID||'","'||
                    B.transaction_id||'","'||
                    rsl.SHIPMENT_LINE_ID||'","'||
                    C.RECEIPT_NUM||'","'||
                    B.TRANSACTION_DATE||'","'||
                    hl.description||'","'||
                    C.ATTRIBUTE1||'","'||
                    C.ATTRIBUTE2
                    from 
                    RCV_TRANSACTIONS B,
                    RCV_Shipment_HEADERS C,
                    rcv_shipment_lines rsl,
                    HR_ALL_ORGANIZATION_UNITS HAOU,
                    HR_ORGANIZATION_UNITS_V hou, 
                    HR_LOCATIONS HL
                    WHERE 1=1
                    AND B.SHIPMENT_HEADER_ID=C.SHIPMENT_HEADER_ID
                    AND B.TRANSACTION_TYPE='RECEIVE'
                    AND C.RECEIPT_SOURCE_CODE='INTERNAL ORDER'
                    AND C.ORGANIZATION_ID=HAOU.ORGANIZATION_ID
                    AND HAOU.LOCATION_ID=HL.LOCATION_ID
                    AND C.SHIP_TO_ORG_ID = HOU.ORGANIZATION_ID
                    AND B.SHIPMENT_HEADER_ID=C.SHIPMENT_HEADER_ID-----
                    and B.SHIPMENT_LINE_ID = rsl.SHIPMENT_LINE_ID-----
                    AND C.SHIP_TO_ORG_ID = '{inventory_org}'
                    and b.ORGANIZATION_ID = '{inventory_org}'
                    AND C.SHIPMENT_HEADER_ID= NVL('{mrn_no}',C.SHIPMENT_HEADER_ID)
                    AND B.TRANSACTION_DATE>= '{from_date}'
                    AND B.TRANSACTION_DATE<tO_DATE('{to_date}')+1
                    and nvl(c.attribute6,'aaa') = nvl('{gate_entry_no}',nvl(c.attribute6,'aaa'))
                    AND ('{item_category}' = 'ISO' OR NVL('{item_category}','All') = 'All')
                    AND C.ORGANIZATION_ID = NVL('{vender}',C.ORGANIZATION_ID)
                    ) A 
                    --order by A.TRANSACTION_DATE
"""
    cur = cursor_ora.execute(list_data)
    print(cur)
    MRN_DATA = cur.fetchall()
    rplc_left = str(MRN_DATA).replace("('", '("')
    rplc_right = rplc_left.replace("',)", '")')
    print(rplc_right)
    rplc_single_quote = rplc_right.replace("'", "pipe")
    rplc_double_quote = rplc_single_quote.replace('"', "'")
    rplc_pip_to_quote = rplc_double_quote.replace("pipe", '"')
    res = rplc_pip_to_quote[1:-1]
    conn_db = psycopg2.connect(user="oracle_user", password="password", host="127.0.0.1", port="5433",
                                      database="oracle_db")
    cursor = conn_db.cursor()
    try:
        if table_type == 'create_table':
            print(table_type)
            try:
                cursor.execute(table_create)
                conn_db.commit()
                return JsonResponse({"Message": f" Table  {TABLE_NAME} Created  Successfully"})
            except Exception as e:
                return JsonResponse({"Error": e})
        if table_type == 'insert':
            print(table_type,'table_typetable_typetable_type')
            try:
                sql_stat = f"""INSERT INTO {TABLE_NAME}  (ge_number,
                            ge_date,
                            ORGANIZATION_ID,
                            orgname,
                            ATTRIBUTE7,
                            SHIPMENT_HEADER_ID,
                            transaction_id,
                            SHIPMENT_LINE_ID,
                            RECEIPT_NUM,
                            CREATION_DATE,
                            VENDOR_NAME,
                            ATTRIBUTE1,
                            ATTRIBUTE2)
                            VALUES {res}"""
                cursor.execute(sql_stat)
                conn_db.commit()
                print(conn_db)
                return JsonResponse({"Message": f" In  {TABLE_NAME},  Data inserted  Successfully!!!"})
            except Exception as e:
                return JsonResponse({"Error": e})
        if table_type == 'create&insert':
            print(table_type)
            try:
                cursor.execute(table_create)
                conn_db.commit()
                sql_stat = f"""INSERT INTO {TABLE_NAME}  (ge_number,
                            ge_date,
                            ORGANIZATION_ID,
                            orgname,
                            ATTRIBUTE7,
                            SHIPMENT_HEADER_ID,
                            transaction_id,
                            SHIPMENT_LINE_ID,
                            RECEIPT_NUM,
                            CREATION_DATE,
                            VENDOR_NAME,
                            ATTRIBUTE1,
                            ATTRIBUTE2)
                            VALUES {res}"""
                cursor.execute(sql_stat)
                conn_db.commit()
                print(conn_db)
                return JsonResponse({"Message": f" Table {TABLE_NAME} Created & Data inserted  Successfully!!!"})
            except Exception as e:
                return JsonResponse({"Error": e})

        if table_type=='replace':
            print(table_type)
            try:
                drop_table = f"DROP TABLE {REPLACE_TABLE_NAME}"
                cursor.execute(drop_table)
                conn_db.commit()
                cursor.execute(table_create)
                conn_db.commit()
                sql_stat = f"""INSERT INTO {TABLE_NAME} (ge_number,
                            ge_date,
                            ORGANIZATION_ID,
                            orgname,
                            ATTRIBUTE7,
                            SHIPMENT_HEADER_ID,
                            transaction_id,
                            SHIPMENT_LINE_ID,
                            RECEIPT_NUM,
                            CREATION_DATE,
                            VENDOR_NAME,
                            ATTRIBUTE1,
                            ATTRIBUTE2)
                            VALUES {res}"""
                cursor.execute(sql_stat)
                conn_db.commit()
                return JsonResponse({"Message": f"Table {REPLACE_TABLE_NAME} removed and "
                                                f"Table  {TABLE_NAME} Created  & Data inserted  Successfully!!!"})
            except Exception as e:
                return JsonResponse({"Error": e})

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating PostgreSQL table", error)
    context = {
        "MRN_DATA": MRN_DATA
    }
    return render(request, 'app/app/mrn_status_report.html')

@api_view(['POST'])
def download_mrn_status_report(request):
    '''
    Download the report from postgres database
    :param request:
    :return:
    '''
    data = request.data
    report_type = data['report_type']
    inventory_org = data['inventory_org']
    from_date = data['from_date']
    print(from_date)
    to_date = data['to_date']
    vender = data['vender']
    ge_number = data['gate_entry_no']
    cursor = connection.cursor()
    sql_statement = f'''SELECT * FROM  public.{TABLE_NAME} WHERE (to_date(creation_date,'DD-MON-YY') between 
    '{from_date}' and  '{to_date}') 
    and ('{vender}'='' OR vendor_name = '{vender}')
    and ('{inventory_org}'='' OR organization_id = '{inventory_org}');
    --and ('{ge_number}'='' OR ge_number = '{ge_number}');
'''

    cursor.execute(sql_statement)
    row_data = cursor.fetchall()
    output = BytesIO()
    if report_type == 'excel':
        workbook = xlsxwriter.Workbook(output, {'constant_memory': True})
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})
        headings = ['ge_number','ge_date','ORGANIZATION_ID' ,'orgname','ATTRIBUTE7','SHIPMENT_HEADER_ID',
                    'transaction_id','SHIPMENT_LINE_ID' ,'RECEIPT_NUM','CREATION_DATE','VENDOR_NAME',
                    'ATTRIBUTE1','ATTRIBUTE2']
        col = 0
        for row, data in enumerate(row_data):
            worksheet.write_row('A1', headings, bold)
            worksheet.write_row(row+1, col, data)
        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        return response
    if report_type == 'pdf':
        return HttpResponse("PENDING")


def mrn_report_download_parameter(request):
    '''
    Front view  to download the report
    :param request:
    :return:
    '''
    form = MRNReportDownloadForm(request.POST or None)
    if form.is_valid():
        data = form.save(commit=False)
        form.save()
        return redirect('')
    else:
        print(form.errors)
    return render(request, 'app/app/mrn_report_download_parameter.html', {'form': form})