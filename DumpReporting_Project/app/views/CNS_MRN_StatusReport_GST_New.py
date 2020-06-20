from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import xlsxwriter
import cx_Oracle
from io import BytesIO, StringIO
from app.forms import MRNReportGSTNewForm
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import psycopg2
from django.contrib import messages
TABLE_REPORT_NAME = "public.dump_table_report"
from django.db import connection
from datetime import datetime

def mrn_status_report_gst_parameter(request):
    '''
    Create front view to access the data from the oracle DB..
    :param request:
    :return:
    '''
    form = MRNReportGSTNewForm(request.POST or None)
    if form.is_valid():
        data = form.save(commit=False)
        form.save()
        return redirect('.')
    else:
        print(form.errors)
    return render(request, 'app/app/mrn_report_gst_parameter.html', {'form': form})


@api_view(['POST'])
def mrn_status_report_gst_new_view(request):
    data = request.data
    print(data,'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
    dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
    connection_oracle = cx_Oracle.connect(user=r'apps', password='apps1234', dsn=dsn_tns, encoding="UTF-8")
    cursor_conn = connection_oracle.cursor()
    print(cursor_conn,'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
    listdata=f"""SELECT q1.SHIPMENT_HEADER_ID, q2.SHIPMENT_LINE_ID
                FROM (SELECT
                rt.Transaction_type,
                rt.Transaction_id,
                A.SHIPMENT_HEADER_ID,
                A.routing_header_id,
                F.receipt_num,
                F.attribute6,
                substr(F.attribute8,0,10) attribute8,
                F.ATTRIBUTE7 FORM_NO,
                OEH.ORDERED_DATE L_DATE,
                A.source_document_code,
                A.REQUISITION_LINE_ID,
                C.PO_HEADER_ID,
                A.SHIPMENT_LINE_ID,
                A.LINE_NUM,
                B.SEGMENT1,
                A.ITEM_REVISION,
                A.ITEM_ID,
                A.ITEM_DESCRIPTION,
                A.UNIT_OF_MEASURE,
                A.QUANTITY_SHIPPED,
                APPS.XX_REC_QTY_func(A.SHIPMENT_LINE_ID,'REC') Quantity_received,
                APPS.XX_REC_QTY_func(A.SHIPMENT_LINE_ID,'NET_RTV') net_rtv,
                APPS.XX_REC_QTY_func(A.SHIPMENT_LINE_ID,'NET_REC') Net_received,
                APPS.XX_REC_QTY_func(A.SHIPMENT_LINE_ID,'REJ') rejected_Quantity,
                OEH.ORDER_NUMBER SEGMENT1,
                E.WIP_ENTITY_NAME JOB_NO
                FROM RCV_TRANSACTIONS rt,
                RCV_SHIPMENT_LINES A,
                RCV_SHIPMENT_HEADERS F,
                MTL_SYSTEM_ITEMS B,
                po_headers_all c,
                PO_DISTRIBUTIONS_all D,
                PO_REQUISITION_LINES_ALL PRL,
                PO_REQUISITION_HEADERS_ALL PRH,
                oe_order_headers_all oeh,
                WIP_ENTITIES E
                WHERE A.ITEM_ID=B.INVENTORY_ITEM_ID(+)
                --and a.shipment_header_id = '12109788'
                --AND B.INVENTORY_ITEM_ID = NVL(:P_ITEM,B.INVENTORY_ITEM_ID)
                AND A.SHIPMENT_HEADER_ID = F.SHIPMENT_HEADER_ID
                AND A.REQUISITION_LINE_ID = PRL.REQUISITION_LINE_ID
                AND PRL.REQUISITION_HEADER_ID = PRH.REQUISITION_HEADER_ID
                AND oeH.ORIG_SYS_DOCUMENT_REF=PRH.SEGMENT1
                AND B.ORGANIZATION_ID(+)= 395
                AND OEH.ORG_ID = (SELECT OPERATING_UNIT FROM ORG_ORGANIZATION_DEFINITIONS WHERE ORGANIZATION_ID = F.ORGANIZATION_ID)
                and a.po_header_id=c.po_header_id(+)
                AND D.PO_DISTRIBUTION_ID(+)=A.PO_DISTRIBUTION_ID
                AND E.WIP_ENTITY_ID(+)=D.WIP_ENTITY_ID
                AND A.source_document_code = 'REQ'
                AND F.SHIPMENT_HEADER_ID=RT.SHIPMENT_HEADER_ID
                and rt.SHIPMENT_LINE_ID = A.SHIPMENT_LINE_ID
                AND rt.TRANSACTION_TYPE='RECEIVE'
                --and rt.ORGANIZATION_ID = F.ORGANIZATION_ID
                UNION ALL
                SELECT
                rt.Transaction_type,
                rt.Transaction_id,
                A.SHIPMENT_HEADER_ID,
                A.routing_header_id,
                F.receipt_num,
                F.attribute6,
                substr(F.attribute8,0,10) attribute8,
                F.ATTRIBUTE7 FORM_NO,
                C.CREATION_DATE L_DATE,
                A.source_document_code,
                A.REQUISITION_LINE_ID,
                C.PO_HEADER_ID,
                A.SHIPMENT_LINE_ID,
                A.LINE_NUM,
                B.SEGMENT1,
                A.ITEM_REVISION,
                A.ITEM_ID,
                A.ITEM_DESCRIPTION,
                A.UNIT_OF_MEASURE,
                A.QUANTITY_SHIPPED,
                APPS.XX_REC_QTY_func(A.SHIPMENT_LINE_ID,'REC') Quantity_received,
                APPS.XX_REC_QTY_func(A.SHIPMENT_LINE_ID,'NET_RTV') net_rtv,
                APPS.XX_REC_QTY_func(A.SHIPMENT_LINE_ID,'NET_REC') Net_received,
                APPS.XX_REC_QTY_func(A.SHIPMENT_LINE_ID,'REJ') rejected_Quantity,
                TO_NUMBER(C.SEGMENT1) SEGMENT1,
                E.WIP_ENTITY_NAME JOB_NO
                FROM RCV_TRANSACTIONS rt,
                     RCV_SHIPMENT_LINES A,
                     RCV_SHIPMENT_HEADERS F,
                     MTL_SYSTEM_ITEMS B,
                     po_headers_all c,
                     PO_DISTRIBUTIONS_all D,
                     WIP_ENTITIES E
                WHERE A.ITEM_ID=B.INVENTORY_ITEM_ID(+)
                --AND B.INVENTORY_ITEM_ID = NVL(:P_ITEM,B.INVENTORY_ITEM_ID)
                AND F.SHIPMENT_HEADER_ID = A.SHIPMENT_HEADER_ID
                AND B.ORGANIZATION_ID(+)= 395
                and a.po_header_id=c.po_header_id(+)
                AND D.PO_DISTRIBUTION_ID(+)=A.PO_DISTRIBUTION_ID
                AND E.WIP_ENTITY_ID(+)=D.WIP_ENTITY_ID
                --and a.shipment_header_id = '12109788'
                AND A.source_document_code != 'REQ'
                AND A.SHIPMENT_HEADER_ID=RT.SHIPMENT_HEADER_ID
                and rt.SHIPMENT_LINE_ID = A.SHIPMENT_LINE_ID
                AND rt.TRANSACTION_TYPE='RECEIVE'
                --and rt.ORGANIZATION_ID = F.ORGANIZATION_ID
                ) q2,
                (select
                A.* from (
                SELECT --DISTINCT
                c.ATTRIBUTE6 ge_number,
                c.attribute8 ge_date,
                B.ORGANIZATION_ID
                ,(select organization_name from org_organization_definitions where organization_id = b.organization_id) orgname
                ,c.ATTRIBUTE7,
                B.SHIPMENT_HEADER_ID,
                null transaction_id,
                B.SHIPMENT_LINE_ID,
                C.RECEIPT_NUM,
                TRUNC(B.TRANSACTION_DATE) CREATION_DATE,
                pv.VENDOR_NAME,
                C.ATTRIBUTE1,C.ATTRIBUTE2
                from
                PO_HEADERS_all A,
                --PO_LINES_ALL PLA,
                RCV_TRANSACTIONS B,
                RCV_SHIPMENT_HEADERS C,
                --rcv_shipment_lines rsl,
                AP_SUPPLIERS pv,
                WIP_ENTITIES WE
                WHERE A.PO_HEADER_ID=B.PO_HEADER_ID
                --AND A.PO_HEADER_ID = PLA.PO_HEADER_ID
                --AND PLA.LINE_TYPE_ID != '3'
                AND B.SHIPMENT_HEADER_ID=C.SHIPMENT_HEADER_ID
                AND B.TRANSACTION_TYPE='RECEIVE'
                and b.SOURCE_DOCUMENT_CODE='PO'
                AND B.WIP_ENTITY_ID =WE.WIP_ENTITY_ID
                --and b.VENDOR_ID=c.VENDOR_ID
                and c.VENDOR_ID=pv.VENDOR_ID
                AND B.SHIPMENT_HEADER_ID=C.SHIPMENT_HEADER_ID-----
                --AND B.PO_LINE_ID=PLA.PO_LINE_ID
                --and b.ORGANIZATION_ID = 395
                --AND C.SHIPMENT_HEADER_ID= NVL(:P_MRN_NO,C.SHIPMENT_HEADER_ID)
                --AND trunc(B.TRANSACTION_DATE)>=nvl('01-FEB-20', trunc(B.TRANSACTION_DATE))
                --AND  trunc(B.TRANSACTION_DATE)<=  nvl('10-FEB-20', trunc(B.TRANSACTION_DATE))
                --AND pv.vendor_id = nvl(:p_vendor_id,pv.vendor_id)
                --and A.po_header_id = nvl(:p_po_number,A.po_header_id)
                --and nvl(c.attribute6,'aaa') = nvl(:p_ge_no,nvl(c.attribute6,'aaa'))
                --AND NVL(:P_ITEM_CATEGORY,'All') in ('Jobwork','All')
                AND B.TRANSACTION_DATE>=  to_date('01-FEB-20', 'DD-MON-YY')
                AND B.TRANSACTION_DATE<  to_date('10-FEB-20')+1
                and c.ship_to_org_id = 395
                UNION ALL
                SELECT --DISTINCT
                c.ATTRIBUTE6 ge_number,
                c.attribute8 ge_date,
                B.ORGANIZATION_ID
                ,(select organization_name from org_organization_definitions where organization_id = b.organization_id) orgname
                ,c.ATTRIBUTE7,
                B.SHIPMENT_HEADER_ID,
                null transaction_id,
                B.SHIPMENT_LINE_ID,
                C.RECEIPT_NUM,
                TRUNC(B.TRANSACTION_DATE) CREATION_DATE,
                pv.VENDOR_NAME,
                C.ATTRIBUTE1,C.ATTRIBUTE2
                from
                PO_HEADERS_all A,
                --PO_LINES_ALL PLA,
                RCV_TRANSACTIONS B,
                RCV_SHIPMENT_HEADERS C,
                --rcv_shipment_lines rsl,
                AP_SUPPLIERS pv
                WHERE A.PO_HEADER_ID=B.PO_HEADER_ID
                --AND A.PO_HEADER_ID = PLA.PO_HEADER_ID
                --AND PLA.LINE_TYPE_ID != '3'
                AND B.SHIPMENT_HEADER_ID=C.SHIPMENT_HEADER_ID
                AND B.TRANSACTION_TYPE='RECEIVE'
                and b.SOURCE_DOCUMENT_CODE='PO'
                AND B.WIP_ENTITY_ID IS NULL
                --and b.VENDOR_ID=c.VENDOR_ID
                and c.VENDOR_ID=pv.VENDOR_ID
                AND B.SHIPMENT_HEADER_ID=C.SHIPMENT_HEADER_ID-----
                --AND B.PO_LINE_ID=PLA.PO_LINE_ID
                --and b.ORGANIZATION_ID = 395
                --AND C.SHIPMENT_HEADER_ID= NVL(:P_MRN_NO,C.SHIPMENT_HEADER_ID)
                --AND trunc(B.TRANSACTION_DATE)>=nvl('01-FEB-20', trunc(B.TRANSACTION_DATE))
                --AND  trunc(B.TRANSACTION_DATE)<=  nvl('10-FEB-20', trunc(B.TRANSACTION_DATE))
                --AND pv.vendor_id = nvl(:p_vendor_id,pv.vendor_id)
                --and A.po_header_id = nvl(:p_po_number,A.po_header_id)
                --and nvl(c.attribute6,'aaa') = nvl(:p_ge_no,nvl(c.attribute6,'aaa'))
                --AND NVL(:P_ITEM_CATEGORY,'All') in ('Purchase','All')
                AND B.TRANSACTION_DATE>=  to_date('01-FEB-20')
                AND B.TRANSACTION_DATE<  to_date('10-FEB-20')+1
                and c.ship_to_org_id = 395
                --ORDER BY CREATION_DATE
                union all
                SELECT c.ATTRIBUTE6 ge_number,
                c.attribute8 ge_date,
                B.ORGANIZATION_ID,
                (select organization_name from org_organization_definitions where organization_id = b.organization_id) orgname
                ,c.ATTRIBUTE7,
                B.SHIPMENT_HEADER_ID,
                null transaction_id,
                B.SHIPMENT_LINE_ID,
                C.RECEIPT_NUM,
                B.TRANSACTION_DATE CREATION_DATE,
                ac.customer_NAME VENDOR_NAME,
                C.ATTRIBUTE1,C.ATTRIBUTE2
                from
                   RCV_TRANSACTIONS B,
                   RCV_Shipment_HEADERS C,
                    ar_customers ac
                WHERE 1=1
                AND B.SHIPMENT_HEADER_ID=C.SHIPMENT_HEADER_ID
                AND C.SHIP_TO_ORG_ID = 395
                AND B.TRANSACTION_TYPE='RECEIVE'
                and b.SOURCE_DOCUMENT_CODE='RMA'
                and c.customer_ID=ac.customer_ID
                --AND B.SHIPMENT_HEADER_ID= NVL(:P_MRN_NO,B.SHIPMENT_HEADER_ID)
                --AND trunc(B.TRANSACTION_DATE)>=nvl('01-FEB-20', trunc(B.TRANSACTION_DATE))
                --AND trunc(B.TRANSACTION_DATE)<=  nvl('10-FEB-20', trunc(B.TRANSACTION_DATE))
                AND B.TRANSACTION_DATE>=  to_date('01-FEB-20')
                AND B.TRANSACTION_DATE<  to_date('10-FEB-20')+1
                --and  ac.customer_id = nvl(:p_vendor_id,ac.customer_id)
                --and  nvl(c.attribute6,'aaa') = nvl(:p_ge_no, nvl(c.attribute6,'aaa'))
                --AND NVL(:P_ITEM_CATEGORY,'All') in ('RMA','All')
                union all
                SELECT  c.ATTRIBUTE6 ge_number,
                c.attribute8 ge_date,
                B.ORGANIZATION_ID,
                (select organization_name from org_organization_definitions where organization_id = b.organization_id) orgname
                ,c.ATTRIBUTE7,
                B.SHIPMENT_HEADER_ID,
                null transaction_id,
                B.SHIPMENT_LINE_ID,
                C.RECEIPT_NUM,
                B.TRANSACTION_DATE CREATION_DATE,
                hl.description VENDOR_NAME,
                C.ATTRIBUTE1,C.ATTRIBUTE2
                from
                RCV_TRANSACTIONS B,
                RCV_Shipment_HEADERS C,
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
                --AND trunc(B.TRANSACTION_DATE)>=nvl('01-FEB-20', trunc(B.TRANSACTION_DATE))
                --AND  trunc(B.TRANSACTION_DATE)<=  nvl('10-FEB-20', trunc(B.TRANSACTION_DATE))
                --AND NVL(:P_ITEM_CATEGORY,'All') in ('ISO','All')
                --AND C.ORGANIZATION_ID = NVL(:P_VENDOR_ID,C.ORGANIZATION_ID)
                AND B.TRANSACTION_DATE>=  to_date('01-FEB-20')
                AND B.TRANSACTION_DATE<  to_date('10-FEB-20')+1
                AND C.SHIP_TO_ORG_ID = 395
                ) A
                where 1 = 1
                group by GE_NUMBER, GE_DATE, ORGANIZATION_ID, ORGNAME, ATTRIBUTE7, SHIPMENT_HEADER_ID, TRANSACTION_ID, SHIPMENT_LINE_ID, RECEIPT_NUM, CREATION_DATE, VENDOR_NAME, ATTRIBUTE1, ATTRIBUTE2) q1
                where q1.SHIPMENT_HEADER_ID = q2.SHIPMENT_HEADER_ID
                and q1.SHIPMENT_LINE_ID = q2.SHIPMENT_LINE_ID"""
    cur = cursor_conn.execute(listdata)
    print(cur)
    MRN_DATA = cur.fetchall()
    rplc_left = str(MRN_DATA).replace("('", '("')
    rplc_right = rplc_left.replace("',)", '")')
    rplc_single_quote = rplc_right.replace("'", "pipe")
    rplc_double_quote = rplc_single_quote.replace('"', "'")
    rplc_pip_to_quote = rplc_double_quote.replace("pipe", '"')
    res = rplc_pip_to_quote[1:-1]
    print(res,'ssssssssssssssssssssssssssssssssssssss')
    conn_db = psycopg2.connect(user="oracle_user", password="password", host="127.0.0.1", port="5433",
                                      database="oracle_db")

    cursor = conn_db.cursor()
    return render(request, 'app/app/mrn_status_gst_new_report.html')

