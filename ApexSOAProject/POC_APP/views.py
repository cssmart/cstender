from django.core.mail import EmailMessage
from xhtml2pdf import pisa # import python module
from django.template.loader import get_template
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from datetime import datetime
from django.db import connection
import cx_Oracle
from io import BytesIO, StringIO
import string
from django.shortcuts import redirect, render_to_response, get_object_or_404, render




@api_view(['POST'])
def POC_view(request):
    data = request.data
    PO_ID = data['PO_ID'] or None
    PO_NO = data['PO_NO'] or None
    SUPPLIER = data['SUPPLIER'] or None
    AMOUNT = data['AMOUNT'] or None


    url = f'http://127.0.0.1:8000/{PO_ID}'
    url_create = url.translate({ord(c): '%20' for c in string.whitespace})
    ctx = {
        'PO_ID': PO_ID,
        'PO_NO': PO_NO,
        'SUPPLIER': SUPPLIER,
        'AMOUNT': AMOUNT,
        'url_create':url_create,
    }
    message = get_template('POC/pop.html').render(ctx)
    msg = EmailMessage(
        f'Awaiting approval for PO.',
        message,
        'apex.mailer@cselectric.co.in',  # will be change
        # ['harshita.agarwal@cselectric.co.in ', 'puneet.kumar@cselectric.co.in'],
        ['harshita.agarwal@cselectric.co.in'],
        # [EMAIL],
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    message_response = f'Mail has been delivered , Thank You!!'
    return JsonResponse({'Message': message_response})


def POC_MORE_DETAIL_INFO(request, pid):
    dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
    conn_ora = cx_Oracle.connect(user=r'APEX_EBS_EXTENSION', password='sbapex123', dsn=dsn_tns)
    cursor = conn_ora.cursor()
    # query = f'''
    #          select * from APEX_PO_APPROVAL where PO_ID  = '{pid}'
    #       '''
    query = f'''select distinct a.DOCUMENT_NO as PO_NO
      ,line_type as line_type
      ,line_num as shipment_number
      ,(SELECT X.segment1 FROM APPS.MTL_SYSTEM_ITEMS_B X WHERE X.INVENTORY_ITEM_ID=A.ITEM_ID AND X.ORGANIZATION_ID=112) as Item
      ,a.REVISION_NUM as revision
      ,a.item_description as description
      ,a.CAT as Category
      ,a.QUANTITY as Qty
      ,a.UNIT_PRICE 
      ,nvl(a.UNIT_PRICE,0)*nvl(a.QUANTITY,0) as base_amount
      ,a.NEED_BY_DATE 
      ,a.NONREVOVERABLE_TAXES
      ,a.REVOVERABLE_TAXES
      ,round(a.AVG_COST,5) avg_cost
      ,a.SHIP_PLANT
      ,a.LOCATION_CODE
	  ,a.PO_SOURCE
		      ,a.CURRENCY_CODE currency
      ,a.UOM
      ,nvl((select rate from apps.po_distributions_all X
            where X.po_line_id= a.po_line_id
                   AND X.ORG_ID=A.ORG_ID
              and rownum=1),nvl((select rate from apps.po_headers_all X
            where X.po_header_id= a.po_header_id
                   AND X.ORG_ID=A.ORG_ID
              and rownum=1),1) ) CONV_RATE
      ,(select SUM(QUANTITY)
 from apps.PO_REQUISITION_LINES_all R 
      ,apps.PO_REQUISITION_HEADERS_all  z
WHERE R.REQUISITION_HEADER_ID = z.REQUISITION_HEADER_ID
AND NVL(R.CANCEL_FLAG,'N')='N'
AND R.LINE_LOCATION_ID IS NULL
  AND ((z.AUTHORIZATION_STATUS = 'APPROVED' and NVL(R.REQS_IN_POOL_FLAG,'N') = 'Y') or z.AUTHORIZATION_STATUS = 'RETURNED')
  AND R.ITEM_ID = a.ITEM_ID
  AND R.ORG_ID = a.ORG_ID
  and r.DESTINATION_ORGANIZATION_ID=a.organization_id) "Pending PR Qty",
     (SELECT SUM(X.PRIMARY_TRANSACTION_QUANTITY)
       FROM APPS.MTL_ONHAND_QUANTITIES_DETAIL X,APPS.MTL_SECONDARY_INVENTORIES Y
      WHERE X.SUBINVENTORY_CODE=Y.SECONDARY_INVENTORY_NAME
        AND X.ORGANIZATION_ID=Y.ORGANIZATION_ID
AND Y.ASSET_INVENTORY=1
AND X.INVENTORY_ITEM_ID=A.ITEM_ID
AND X.ORGANIZATION_ID=NVL(A.ORGANIZATION_ID,X.ORGANIZATION_ID)
) STK,
(SELECT X.PRIMARY_UOM_CODE
       FROM APPS.MTL_SYSTEM_ITEMS X
      WHERE X.INVENTORY_ITEM_ID=A.ITEM_ID
AND X.ORGANIZATION_ID=NVL(A.ORGANIZATION_ID,X.ORGANIZATION_ID)
AND ROWNUM=1
) STK_UOM,
(SELECT min(FORWARD_ON)
FROM APEX_EBS_EXTENSION.XXAPX_PO_APROVAL_TRANSACTION
WHERE ENITITY_TRX_ID=A.PO_HEADER_ID
  and NVL(release_id,-1) = NVL(a.po_release_id,-1)
) STK_DATE,
 (SELECT MSS.SAFETY_STOCK_QUANTITY
   from APPS.MTL_SAFETY_STOCKS MSS
  where 1=1
     and mss.inventory_item_id = A.ITEM_ID
      and mss.organization_id = A.ORGANIZATION_ID
      and mss.EFFECTIVITY_DATE = (select max(mss1.EFFECTIVITY_DATE)
                                    from APPS.MTL_SAFETY_STOCKS mss1
                                   where mss1.inventory_item_id=mss.inventory_item_id
                                     AND mss1.organization_id=mss.organization_id
                                 )) SAFETY_STOCK,
(select MIN_MINMAX_QUANTITY from apps.mtl_system_items_b where INVENTORY_ITEM_ID=A.ITEM_ID and ORGANIZATION_ID=A.ORGANIZATION_ID) MIN_QTY,
(select MAX_MINMAX_QUANTITY from apps.mtl_system_items_b where INVENTORY_ITEM_ID=A.ITEM_ID and ORGANIZATION_ID=A.ORGANIZATION_ID) MAX_QTY,
---(select count(distinct DOCUMENT_NO) from apps.xxcns_po_details_v where ITEM_ID =a.item_id) pending_po_qty
(select --count(*) 
 		sum(plla.QUANTITY)
     from apps.po_lines_all pla,apps.po_headers_All pha,
          apps.po_line_locations_all plla
    where 1=1
      and pla.po_line_id = plla.po_line_id
 and pla.po_header_id=pha.po_header_id
 and pha.AUTHORIZATION_STATUS='APPROVED'
 and pha.TYPE_LOOKUP_CODE not in ('BLANKET', 'PLANNED')
      and pla.ITEM_ID = A.ITEM_ID
      and pla.org_id = a.org_id
      and nvl(pla.CLOSED_CODE,'OPEN') = 'OPEN'
      and nvl(plla.CLOSED_CODE,'OPEN') = 'OPEN') pending_po_qty
from apps.XXCNS_PO_DETAILS_V a
where trim(a.po_header_id)='634774'
           '''
    cursor.execute(query)
    MRN_DATA = cursor.fetchall()
    try:
        for i in MRN_DATA:
            id = i[0]
            PO_NO= i[2]
            SUPPLIER= i[4]
            PO_DESC = i[3]
            PO_DATE = i[1]
            ctx ={
               'id': id,
               'PO_NO': PO_NO,
               'SUPPLIER': SUPPLIER,
               'PO_DESC': PO_DESC,
               'PO_DATE': PO_DATE
            }
            return render(request,'POC/more_details_mail_template.html', ctx)
    except ObjectDoesNotExist:
        raise Http404













 # D= [{'PO_ID': 'TEST', 'PO_NUMBER': 1, 'PO_DATE':'23-03-2020','PO_DESC':'DDDDDDDDDDDDDDD','SUPPLIER':'QW'},
   #      {'PO_ID': 'HARSHITA', 'PO_NUMBER': 2, 'PO_DATE':'23-03-2020','PO_DESC':'DDDDDDDDDDDDDDD','SUPPLIER':'QW'}]
   # print(D,'AAAAAAAAAAAAAAAA')

   # def POC_MORE_DETAIL_INFO(request, pid):
   #     print(pid, 'aaa')
   #     dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
   #     conn_ora = cx_Oracle.connect(user=r'APEX_EBS_EXTENSION', password='sbapex123', dsn=dsn_tns)
   #     cursor = conn_ora.cursor()
   #     query = f'''
   #              select * from APEX_PO_APPROVAL where PO_ID  = '{pid}'
   #           '''
   #     # query = f'''
   #     #           select * from APEX_PO_APPROVAL
   #     #        '''
   #     cursor.execute(query)
   #     MRN_DATA = cursor.fetchall()
   #     print(MRN_DATA, 'q111111111122222222222222222222222222222222222222')
   #     list_data = []
   #     # D= [{'PO_ID': 'TEST', 'PO_NUMBER': 1, 'PO_DATE':'23-03-2020','PO_DESC':'DDDDDDDDDDDDDDD','SUPPLIER':'QW'},
   #     #      {'PO_ID': 'HARSHITA', 'PO_NUMBER': 2, 'PO_DATE':'23-03-2020','PO_DESC':'DDDDDDDDDDDDDDD','SUPPLIER':'QW'}]
   #     # print(D,'AAAAAAAAAAAAAAAA')
   #     # context = {
   #     #     'D':D,
   #     # }
   #     # print(context,'aaaaaaaaaaaaaaaaaaaaaaaaaa')
   #     for i in MRN_DATA:
   #         list_data.append(i)
   #         print(list_data, 'list_datalist_datalist_datalist_datalist_data')
   #     context = {
   #         'list_data': list_data,
   #     }
   #     print(context, 'context---------------------------')
   #     #     print(i,'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
   #     #     print(i[0],'eeeeeeeeeeeeeeeeeeeeeeeeee')
   #     #     id = i[0]
   #     #     PO_NO= i[2]
   #     #     SUPPLIER= i[4]
   #     #     PO_DESC = i[3]
   #     #     PO_DATE = i[1]
   #     #     ctx ={
   #     #         'id': id,
   #     #         'PO_NO': PO_NO,
   #     #         'SUPPLIER': SUPPLIER,
   #     #         'PO_DESC': PO_DESC,
   #     #         'PO_DATE': PO_DATE
   #     #     }
   #     #     print(ctx,'qqqqqqqqqwwwwwwwwwaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
   #     return render(request, 'POC/more_details_mail_template.html', context)
   #
   # # D= [{'PO_ID': 'TEST', 'PO_NUMBER': 1, 'PO_DATE':'23-03-2020','PO_DESC':'DDDDDDDDDDDDDDD','SUPPLIER':'QW'},
   # #      {'PO_ID': 'HARSHITA', 'PO_NUMBER': 2, 'PO_DATE':'23-03-2020','PO_DESC':'DDDDDDDDDDDDDDD','SUPPLIER':'QW'}]
   # # print(D,'AAAAAAAAAAAAAAAA')

