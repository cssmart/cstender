from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import xlsxwriter
import cx_Oracle
from io import BytesIO, StringIO
from .forms import DumpForm, DumpDownloadForm
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import psycopg2
from django.contrib import messages
TABLE_REPORT_NAME = "public.dump_table_report"
from django.db import connection
from datetime import datetime

TABLE_NAME = "FEB_5TH_REPORT26"
REPLACE_TABLE_NAME = "Report_NEW_ONE_TWO"


def dump_report_view(request):
    '''
    Create front view to access the data from the oracle DB..
    :param request:
    :return:
    '''
    form = DumpForm(request.POST or None)
    if form.is_valid():
        data = form.save(commit=False)
        business_line = form.cleaned_data['business_line']
        business_unit = form.cleaned_data['business_unit']
        shipping_org = form.cleaned_data['shipping_org']
        from_date = form.cleaned_data['from_date']
        to_date = form.cleaned_data['to_date']
        unit = form.cleaned_data['unit']
        sales_account = form.cleaned_data['sales_account']
        form.save()
        return redirect('.')
    else:
        print(form.errors)
    return render(request, 'app/app/dump_report_create.html', {'form':form})


@api_view(['POST'])
def dump_report_data(request):

    '''
    Used to access the data from Oracle Db and store the tables and data into postgres db
    :param request:
    :return:
    '''

    data = request.data
    table_type = data['table_type']
    print(table_type)
    business_unit = data['business_unit']
    business_line_input = data['business_line']
    from_date = data['from_date']
    to_date = data['to_date']
    unit = data['unit']
    sales_account = data['sales_account']
    dsn_tns = cx_Oracle.makedsn('192.168.100.121', '1525', service_name='SANDBOX')
    output = BytesIO()
    print(output,'222222222222222')
    conn = cx_Oracle.connect(user=r'apps', password='apps1234', dsn=dsn_tns)
    print(conn)
    cursor = conn.cursor()
    print(cursor)
    data = f"""select V.EXCHANGE_RATE||'","'||
      V.BUSINESS_UNIT||'","'||
      V.BUSINESS_LINE||'","'||
      V.EVENT_CLASS_CODE||'","'||
      V.ENTITY_CODE||'","'||
      V.DEL_ORG_ID||'","'||
      MIN(V.DELIVERY_DETAIL_ID)||'","'||
      V.CONSIGNEE_NAME||'","'||
      V.BILL_TO_SITE_USE_ID||'","'||
      V.SHIP_TO_SITE_USE_ID||'","'||
      V.RAC_BILL_TO_CUSTOMER_NAME||'","'||
      V.CUST_ID||'","'||
      V.RAA_BILL_TO_CONCAT_ADDRESS||'","'||
      V.RAA_BILL_TO_POSTAL_CODE||'","'||
      V.RAA_BILL_TO_STATE||'","'||
      TO_CHAR(V.ORDERED_DATE,'DD-MON-YY')||'","'||
      MIN(V.SHIP_TIME)||'","'||
      TO_CHAR(V.TRX_DATE,'DD-MON-YY')||'","'||
      V.TERMS||'","'||
      --V.CUST_PO_NUMBER,
      REPLACE(V.CUST_PO_NUMBER, '''', '')||'","'||
      --'SSSSSSSSSSSSSSSSSSSSSSSSS',
      --V.PROJ||'","'||
      REPLACE(V.PROJ, '''', '')||'","'||
      TO_CHAR(V.CUSTPODATE,'DD-MON-YY')||'","'||
      V.DELIVERY_ID||'","'||
      V.OA_NO||'","'||
      V.ORDER_TYPE||'","'||
      --REPLACE(V.CUR, '''', '')||'","'||
      V.CUR||'","'||
      sum(V.NET)||'","'||
      REPLACE(V.GROSS, '''', '')||'","'||
      --V.GROSS,
      V.GROSS_WEIGHT||'","'||
      V.HEADER_ID||'","'||
      V.SP_INS||'","'||
      --""FW: SPRA for Supertech " Without Electrican Coupon""
      V.VOLUME||'","'||
      V.RAT_TERM_NAME||'","'||
      --REPLACE(V.RAT_TERM_NAME, '''', '')||'","'||
      V.FOB||'","'||
      max(V.GST_DATE)||'","'||
      max(V.GST_TIME)||'","'||
      nvl(v1.INVENTORY_ITEM_ID,V.INVENTORY_ITEM_ID)||'","'||
      NVL(V1.ITEM_CODE,V.ITEM_CODE)||'","'||
      REPLACE(NVL(V1.DESCRIPTION,V.DESCRIPTION),'''', '')||'","'||
      --'wwwwwwwwwwwwwwwwwwwwwwww',
      --REPLACE(V.DESCRIPTION, '''', ''),
      NVL(V1.UNIT_CODE,V.UNIT_CODE)||'","'||
      MIN(V.LINE_NUMBER)||'","'||
      SUM(NVL(V1.QUANTITY,V.QUANTITY))||'","'||
      NVL(V1.UNIT_SELLING_PRICE,V.UNIT_PRICE)||'","'||
      V.CONVERSION_RATE||'","'||
      V.WAYBILL||'","'||
      V.TRX_NUMBER||'","'||
      SUM(V.REVENUE_AMOUNT)||'","'||
      V.REV_UNIT||'","'||
      V.REV_ACCOUNT||'","'||
      V.REV_ACCT_DESC||'","'||
      V.SHIPPING_ORG||'","'||
      V.CUSTOMER_NUMBER||'","'||
      V.SHIP_CUSTOMER||'","'||
      V.SHIP_CUST_GSTN||'","'||
      V.SHIP_CUST_STATE||'","'||
      V.CUSTOMER_CLASS_CODE||'","'||
      V.CUSTOMER_CATEGORY_CODE||'","'||
      V.DOM_IBD||'","'||
      V.ZONE||'","'||
      V.REGION||'","'||
      V.BRANCH||'","'||
      V.COUNTRY||'","'||
      V.SALESREP_ID||'","'||
      V.COMM||'","'||
      V.TRX_CLASS||'","'||
      SUM(V.TAXABLE_VALUE)||'","'||
      V.TAX_INVOICE_NUM||'","'||
      V.RETURN_REASON_CODE||'","'||
      V.RETURN_ORDER_NUM||'","'||
      V.RETURN_INVOICE_NUM||'","'||
      TO_CHAR((max(V.TAX_INVOICE_DATE)),'DD-MON-YY')||'","'||
      V.TRX_ID||'","'||
      MIN(V.TRX_LINE_ID)||'","'||
      V.ORG_ID||'","'||
      V.SUPPLIER_GST_NUMBER||'","'||
      V.SUPPLIER_PAN_NUM||'","'||
      V.CUSTOMER_GST_NUM||'","'||
      V.CUSTOMER_PAN_NUM||'","'||
      SUM(V.CGST)||'","'||
      V.CGST_RATE||'","'||
      SUM(V.SGST)||'","'||
      V.SGST_RATE||'","'||
      SUM(V.IGST)||'","'||
      V.IGST_RATE||'","'||
      V.CURRENCY_CONVERSION_RATE||'","'||
      V.REGIME_CODE||'","'||
      V.GST_EVENT_CLASS_CODE||'","'||
      V.GST_ENTITY_CODE||'","'||
      MIN(V.DET_FACTOR_ID)||'","'||
      V.SUPP_STATE||'","'||
      V.BILL_STATE||'","'||
      SUM(V.FREIGHT)||'","'||
      SUM(V.INSURANCE)||'","'||
      SUM(V.PACKING)||'","'||
      SUM(V.TCS)||'","'||
      V.SALES_PERSON||'","'||
      V.ORDER_CLASS||'","'||
      V.MIS_CAT1||'","'||
      V.MIS_CAT2||'","'||
      V.HSN_SAC||'","'||
      V.ADDRESSEE||'","'||
      V.TAX_CATEGORY_NAME||'","'||
      V.CREDIT_MEMO_NUM||'","'||
      V.CREDIT_MEMO_DATE
    from apps.XXCNS_SALES_RETURN V,
            CNSTECH2.XXCNS_BTBD_ITEM_DETAILS V1
    where V.CUSTOMER_TRX_ID=V1.CUSTOMER_TRX_ID(+)
    AND V.CUSTOMER_TRX_LINE_ID=V1.CUSTOMER_TRX_LINE_ID(+)
    AND trunc(V.trx_date) between '{from_date}' and '{to_date}'
    and V.business_line = NVL('{business_line_input}',business_line) and V.DELIVERY_DETAIL_ID='17602408'
    --and V.business_line = NVL('{business_line_input}',business_line)
    and V.business_unit = NVL('{business_unit}',business_unit)
    and nvl(substr(v.rev_account,1,4),'X') = nvl('{unit}',nvl(substr(v.rev_account,1,4),'X'))
    and nvl(substr(rev_account,6,7),'X') = nvl('{sales_account}',nvl(substr(rev_account,6,7),'X'))
    GROUP BY V.EXCHANGE_RATE,
    V.BUSINESS_UNIT,
    V.BUSINESS_LINE,
    V.EVENT_CLASS_CODE,
    V.ENTITY_CODE,
    V.DEL_ORG_ID,
    V.CONSIGNEE_NAME,
    V.BILL_TO_SITE_USE_ID,
    V.SHIP_TO_SITE_USE_ID,
    V.RAC_BILL_TO_CUSTOMER_NAME,
    V.CUST_ID,
    V.RAA_BILL_TO_CONCAT_ADDRESS,
    V.RAA_BILL_TO_POSTAL_CODE,
    V.RAA_BILL_TO_STATE,
    V.ORDERED_DATE,
    V.TRX_DATE,
    V.TERMS,
    V.CUST_PO_NUMBER,
    V.PROJ,
    V.CUSTPODATE,
    V.DELIVERY_ID,
    V.OA_NO,
    V.ORDER_TYPE,
    V.CUR,
    V.GROSS,
    V.GROSS_WEIGHT,
    V.HEADER_ID,
    V.SP_INS,
    V.VOLUME,
    V.RAT_TERM_NAME,
    V.FOB,
    V.GST_DATE,
    V.GST_TIME,
    nvl(v1.INVENTORY_ITEM_ID,V.INVENTORY_ITEM_ID),
    NVL(V1.ITEM_CODE,V.ITEM_CODE),
    NVL(V1.DESCRIPTION,V.DESCRIPTION),
    NVL(V1.UNIT_CODE,V.UNIT_CODE),
    NVL(V1.UNIT_SELLING_PRICE,V.UNIT_PRICE),
    V.CONVERSION_RATE,
    V.WAYBILL,
    V.TRX_NUMBER,
    V.REV_UNIT,
    V.REV_ACCOUNT,
    V.REV_ACCT_DESC,
    V.SHIPPING_ORG,
    V.CUSTOMER_NUMBER,
    V.SHIP_CUSTOMER,
    V.SHIP_CUST_GSTN,
    V.SHIP_CUST_STATE,
    V.CUSTOMER_CLASS_CODE,
    V.CUSTOMER_CATEGORY_CODE,
    V.DOM_IBD,
    V.ZONE,
    V.REGION,
    V.BRANCH,
    V.COUNTRY,
    V.SALESREP_ID,
    V.COMM,
    V.TRX_CLASS,
    V.TAX_INVOICE_NUM,
    V.RETURN_REASON_CODE,
    V.RETURN_ORDER_NUM,
    V.RETURN_INVOICE_NUM,
    V.TRX_ID,
    V.ORG_ID,
    V.SUPPLIER_GST_NUMBER,
    V.SUPPLIER_PAN_NUM,
    V.CUSTOMER_GST_NUM,
    V.CUSTOMER_PAN_NUM,
    V.CGST_RATE,
    V.SGST_RATE,
    V.IGST_RATE,
    V.CURRENCY_CONVERSION_RATE,
    V.REGIME_CODE,
    V.GST_EVENT_CLASS_CODE,
    V.GST_ENTITY_CODE,
    V.SUPP_STATE,
    V.BILL_STATE,
    V.SALES_PERSON,
    V.ORDER_CLASS,
    V.MIS_CAT1,
    V.MIS_CAT2,
    V.HSN_SAC,
    V.ADDRESSEE,
    V.TAX_CATEGORY_NAME,
    V.CREDIT_MEMO_NUM,
    V.CREDIT_MEMO_DATE"""
    cur = cursor.execute(data)
    print(cur)
    list_data = []
    newData = cur.fetchall()
    rplc_left = str(newData).replace("('", '("')
    rplc_right = rplc_left.replace("',)", '")')
    print(rplc_right)
    rplc_single_quote = rplc_right.replace("'", "pipe")
    rplc_double_quote = rplc_single_quote.replace('"', "'")
    rplc_pip_to_quote = rplc_double_quote.replace("pipe", '"')
    # print(da)
    # AAA = q[:-4]
    # print(AAA)
    # data = AAA + ')]'
    # rplc_data = str(newData).replace("'", '"')
    # cut_data = rplc_data[:-3]
    # data_val = cut_data + ')]'
    # print(data_val, '444444444444444444443333333333333333333333333333444444444444444444444444444444444444444444444444')
    # print(type(data_val), 'oooooo222222222222222222oooooooeeeeeeeeeeoooooooooooooooooooooo')
    res = rplc_pip_to_quote[1:-1]
    # q = data_.replace('""',"''")
    # res = q.replace('"',"'")
    # print(res, 'dddddddddddddddddddddddddddd55555555555555555555555555555555555555555555555555555555555')
    # s = ""
    # for v in str(newData):
    #     s += v
    # if data_val:
    #
    #     for row in data_val:
    #         # print(row,'p00000000000000000000000000000000000000000000000000000000000000000')
    #         aa = " PIPE=== ".join(map(str, row))
    #         # print(aa, 'harshitaharshitaharshitaharshitaharshitaharshitaharshitaharshitaharshita=====================')
    #         aqq = aa.replace("'", "")
    #         # print(aqq,'------------------------------------------------------------')
    #         q = aqq.replace("PIPE===", "','")
    #         # print(q,'dddddddddddddddddddddddddddddddd')
    #         res = "('" + q + "')"
    #         # res = eval(res)
    #         # print(type(res), 'res_dres_dres_dres_dres_dres_dres_dres_dres_dres_d')
    #         # print(res, 'reeeeeeeeeeeeeeeeeeeeeeeeeeeeeees_dres_dres_dres_dres_dres_dres_dres_dres_dres_d')
    # # newData.append()
    # data = [s]
    # print(data, 'lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll')
    # aa = " PIPE=== ".join(map(str, data))
    # print(aa, 'oooooooooooooooooooooooooooooooooowwwwwwwwwwwwwwwwwwwwwwwwwwwwwoooooooooooooooooooooooooooooooo')
    connection = psycopg2.connect(user="dump_user", password="password", host="127.0.0.1", port="5433",
                                  database="dump_report_db")
    cursor = connection.cursor()
    try:
        if table_type == 'create&insert':
            try:
                sql_statement = f""" CREATE TABLE {TABLE_NAME} (EXCHANGE_RATE VARCHAR(300),
                                   BUSINESS_UNIT VARCHAR(300),
                                   BUSINESS_LINE VARCHAR(300),
                                   EVENT_CLASS_CODE VARCHAR(300),
                                   ENTITY_CODE VARCHAR(300),
                                   DEL_ORG_ID VARCHAR(300),
                                    DELIVERY_DETAIL_ID VARCHAR(300),
                                    CONSIGNEE_NAME  VARCHAR(300),
                                    BILL_TO_SITE_USE_ID  VARCHAR(300),
                                    SHIP_TO_SITE_USE_ID  VARCHAR(300),
                                    RAC_BILL_TO_CUSTOMER_NAME  VARCHAR(300),
                                    CUST_ID  VARCHAR(300),
                                    RAA_BILL_TO_CONCAT_ADDRESS  VARCHAR(1200),
                                    RAA_BILL_TO_POSTAL_CODE  VARCHAR(300),
                                    RAA_BILL_TO_STATE  VARCHAR(300),
                                    ORDERED_DATE  VARCHAR(300),
                                    SHIP_TIME  VARCHAR(300),
                                    TRX_DATE  VARCHAR(300),
                                    TERMS  VARCHAR(300),
                                    CUST_PO_NUMBER  VARCHAR(300),
                                    PROJ VARCHAR(300),
                                    CUSTPODATE  VARCHAR(300),
                                    DELIVERY_ID  VARCHAR(300),
                                    OA_NO  VARCHAR(300),
                                    ORDER_TYPE  VARCHAR(300),
                                    CUR  VARCHAR(300),
                                    NET VARCHAR(300),
                                    GROSS  VARCHAR(300),
                                    GROSS_WEIGHT  VARCHAR(300),
                                    HEADER_ID  VARCHAR(300),
                                    SP_INS  VARCHAR(300),
                                    VOLUME  VARCHAR(300),
                                    RAT_TERM_NAME  VARCHAR(300),
                                    FOB  VARCHAR(300),
                                    GST_DATE VARCHAR(300),
                                    GST_TIME   VARCHAR(300),
                                    INVENTORY_ITEM_ID VARCHAR(300),
                                    ITEM_CODE VARCHAR(300),
                                    DESCRIPTION VARCHAR(300),
                                    UNIT_CODE VARCHAR(300),
                                    LINE_NUMBER VARCHAR(300),
                                    QUANTITY VARCHAR(300),
                                    UNIT_PRICE  VARCHAR(300) ,
                                    CONVERSION_RATE  VARCHAR(300),
                                    WAYBILL  VARCHAR(300),
                                    TRX_NUMBER  VARCHAR(300),
                                    REVENUE_AMOUNT VARCHAR(300),
                                    REV_UNIT  VARCHAR(300),
                                    REV_ACCOUNT  VARCHAR(300),
                                    REV_ACCT_DESC  VARCHAR(300),
                                    SHIPPING_ORG  VARCHAR(300),
                                    CUSTOMER_NUMBER  VARCHAR(300),
                                    SHIP_CUSTOMER  VARCHAR(300),
                                    SHIP_CUST_GSTN  VARCHAR(300),
                                    SHIP_CUST_STATE  VARCHAR(300),
                                    CUSTOMER_CLASS_CODE  VARCHAR(300),
                                    CUSTOMER_CATEGORY_CODE  VARCHAR(300),
                                    DOM_IBD  VARCHAR(300),
                                    ZONE  VARCHAR(300),
                                    REGION  VARCHAR(300),
                                    BRANCH  VARCHAR(300),
                                    COUNTRY  VARCHAR(300),
                                    SALESREP_ID  VARCHAR(300),
                                    COMM  VARCHAR(300),
                                    TRX_CLASS  VARCHAR(300),
                                    TAXABLE_VALUE VARCHAR(300),
                                    TAX_INVOICE_NUM  VARCHAR(300),
                                    RETURN_REASON_CODE  VARCHAR(300),
                                    RETURN_ORDER_NUM  VARCHAR(300),
                                    RETURN_INVOICE_NUM  VARCHAR(300),
                                    TAX_INVOICE_DATE VARCHAR(300),
                                    TRX_ID  VARCHAR(300),
                                    TRX_LINE_ID  VARCHAR(300),
                                    ORG_ID VARCHAR(300),
                                    SUPPLIER_GST_NUMBER VARCHAR(300),
                                    SUPPLIER_PAN_NUM VARCHAR(300),
                                    CUSTOMER_GST_NUM VARCHAR(300),
                                    CUSTOMER_PAN_NUM VARCHAR(300),
                                    CGST  VARCHAR(300),
                                    CGST_RATE VARCHAR(300),
                                    SGST  VARCHAR(300),
                                    SGST_RATE VARCHAR(300),
                                    IGST VARCHAR(300),
                                    IGST_RATE VARCHAR(300),
                                    CURRENCY_CONVERSION_RATE VARCHAR(300),
                                    REGIME_CODE VARCHAR(300),
                                    GST_EVENT_CLASS_CODE VARCHAR(300),
                                    GST_ENTITY_CODE VARCHAR(300),
                                    DET_FACTOR_ID VARCHAR(300),
                                    SUPP_STATE VARCHAR(300),
                                    BILL_STATE VARCHAR(300),
                                    FREIGHT VARCHAR(300),
                                    INSURANCE VARCHAR(300),
                                    PACKING VARCHAR(300),
                                    TCS VARCHAR(300),
                                    SALES_PERSON VARCHAR(300),
                                    ORDER_CLASS VARCHAR(300),
                                    MIS_CAT1 VARCHAR(300),
                                    MIS_CAT2 VARCHAR(300),
                                    HSN_SAC VARCHAR(300),
                                    ADDRESSEE VARCHAR(300),
                                    TAX_CATEGORY_NAME VARCHAR(300),
                                    CREDIT_MEMO_NUM VARCHAR(300),
                                    CREDIT_MEMO_DATE VARCHAR(300));"""
                cursor.execute(sql_statement)
                connection.commit()
                print("Table created successfully in PostgreSQL ")
                sql_stat = f"""INSERT INTO {TABLE_NAME} (EXCHANGE_RATE,
                            BUSINESS_UNIT,
                            BUSINESS_LINE,
                            EVENT_CLASS_CODE,
                            ENTITY_CODE,
                            DEL_ORG_ID,
                            DELIVERY_DETAIL_ID,
                            CONSIGNEE_NAME,
                            BILL_TO_SITE_USE_ID,
                            SHIP_TO_SITE_USE_ID,
                            RAC_BILL_TO_CUSTOMER_NAME,
                            CUST_ID,
                            RAA_BILL_TO_CONCAT_ADDRESS,
                            RAA_BILL_TO_POSTAL_CODE,
                            RAA_BILL_TO_STATE,
                            ORDERED_DATE,
                            SHIP_TIME,
                            TRX_DATE,
                            TERMS,
                            CUST_PO_NUMBER,
                            PROJ,
                            CUSTPODATE,
                            DELIVERY_ID,
                            OA_NO,
                            ORDER_TYPE,
                            CUR,
                            NET,
                            GROSS,
                            GROSS_WEIGHT,
                            HEADER_ID,
                            SP_INS,
                            VOLUME,
                            RAT_TERM_NAME,
                            FOB,
                            GST_DATE,
                            GST_TIME,
                            INVENTORY_ITEM_ID,
                            ITEM_CODE,
                            DESCRIPTION,
                            UNIT_CODE,
                            LINE_NUMBER,
                            QUANTITY,
                            UNIT_PRICE ,
                            CONVERSION_RATE,
                            WAYBILL,
                            TRX_NUMBER,
                            REVENUE_AMOUNT,
                            REV_UNIT,
                            REV_ACCOUNT,
                            REV_ACCT_DESC,
                            SHIPPING_ORG,
                            CUSTOMER_NUMBER,
                            SHIP_CUSTOMER,
                            SHIP_CUST_GSTN,
                            SHIP_CUST_STATE,
                            CUSTOMER_CLASS_CODE,
                            CUSTOMER_CATEGORY_CODE,
                            DOM_IBD,
                            ZONE,
                            REGION,
                            BRANCH,
                            COUNTRY,
                            SALESREP_ID,
                            COMM,
                            TRX_CLASS,
                            TAXABLE_VALUE,
                            TAX_INVOICE_NUM,
                            RETURN_REASON_CODE,
                            RETURN_ORDER_NUM,
                            RETURN_INVOICE_NUM,
                            TAX_INVOICE_DATE,
                            TRX_ID,
                            TRX_LINE_ID,
                            ORG_ID,
                            SUPPLIER_GST_NUMBER,
                            SUPPLIER_PAN_NUM,
                            CUSTOMER_GST_NUM,
                            CUSTOMER_PAN_NUM,
                            CGST,
                            CGST_RATE,
                            SGST,
                            SGST_RATE,
                            IGST,
                            IGST_RATE,
                            CURRENCY_CONVERSION_RATE,
                            REGIME_CODE,
                            GST_EVENT_CLASS_CODE,
                            GST_ENTITY_CODE,
                            DET_FACTOR_ID,
                            SUPP_STATE,
                            BILL_STATE,
                            FREIGHT,
                            INSURANCE,
                            PACKING,
                            TCS,
                            SALES_PERSON,
                            ORDER_CLASS,
                            MIS_CAT1,
                            MIS_CAT2,
                            HSN_SAC,
                            ADDRESSEE,
                            TAX_CATEGORY_NAME,
                            CREDIT_MEMO_NUM,
                            CREDIT_MEMO_DATE)
                            VALUES {res};"""
                cursor.execute(sql_stat)
                connection.commit()
                return JsonResponse(
                    {"Message": f" Table  {TABLE_NAME} Created and Data inserted in {TABLE_NAME} Successfully"})
            except Exception as e:
                return JsonResponse({"Error": e})

        elif table_type == 'create_table':
            try:
                create_statement =f""" CREATE TABLE {TABLE_NAME} (EXCHANGE_RATE VARCHAR(300),
                                   BUSINESS_UNIT VARCHAR(300),
                                   BUSINESS_LINE VARCHAR(300),
                                   EVENT_CLASS_CODE VARCHAR(300),
                                   ENTITY_CODE VARCHAR(300),
                                   DEL_ORG_ID VARCHAR(300),
                                    DELIVERY_DETAIL_ID VARCHAR(300),
                                    CONSIGNEE_NAME  VARCHAR(300),
                                    BILL_TO_SITE_USE_ID  VARCHAR(300),
                                    SHIP_TO_SITE_USE_ID  VARCHAR(300),
                                    RAC_BILL_TO_CUSTOMER_NAME  VARCHAR(300),
                                    CUST_ID  VARCHAR(300),
                                    RAA_BILL_TO_CONCAT_ADDRESS  VARCHAR(1200),
                                    RAA_BILL_TO_POSTAL_CODE  VARCHAR(500),
                                    RAA_BILL_TO_STATE  VARCHAR(300),
                                    ORDERED_DATE  VARCHAR(300),
                                    SHIP_TIME  VARCHAR(300),
                                    TRX_DATE  VARCHAR(300),
                                    TERMS  VARCHAR(300),
                                    CUST_PO_NUMBER  VARCHAR(300),
                                    PROJ VARCHAR(300),
                                    CUSTPODATE  VARCHAR(300),
                                    DELIVERY_ID  VARCHAR(300),
                                    OA_NO  VARCHAR(300),
                                    ORDER_TYPE  VARCHAR(300),
                                    CUR  VARCHAR(300),
                                    NET VARCHAR(300),
                                    GROSS  VARCHAR(300),
                                    GROSS_WEIGHT  VARCHAR(300),
                                    HEADER_ID  VARCHAR(300),
                                    SP_INS  VARCHAR(300),
                                    VOLUME  VARCHAR(300),
                                    RAT_TERM_NAME  VARCHAR(300),
                                    FOB  VARCHAR(300),
                                    GST_DATE VARCHAR(300),
                                    GST_TIME   VARCHAR(300),
                                    INVENTORY_ITEM_ID VARCHAR(300),
                                    ITEM_CODE VARCHAR(300),
                                    DESCRIPTION VARCHAR(300),
                                    UNIT_CODE VARCHAR(300),
                                    LINE_NUMBER VARCHAR(300),
                                    QUANTITY VARCHAR(300),
                                    UNIT_PRICE  VARCHAR(300) ,
                                    CONVERSION_RATE  VARCHAR(300),
                                    WAYBILL  VARCHAR(300),
                                    TRX_NUMBER  VARCHAR(300),
                                    REVENUE_AMOUNT VARCHAR(300),
                                    REV_UNIT  VARCHAR(300),
                                    REV_ACCOUNT  VARCHAR(300),
                                    REV_ACCT_DESC  VARCHAR(300),
                                    SHIPPING_ORG  VARCHAR(300),
                                    CUSTOMER_NUMBER  VARCHAR(300),
                                    SHIP_CUSTOMER  VARCHAR(300),
                                    SHIP_CUST_GSTN  VARCHAR(300),
                                    SHIP_CUST_STATE  VARCHAR(300),
                                    CUSTOMER_CLASS_CODE  VARCHAR(300),
                                    CUSTOMER_CATEGORY_CODE  VARCHAR(300),
                                    DOM_IBD  VARCHAR(300),
                                    ZONE  VARCHAR(300),
                                    REGION  VARCHAR(300),
                                    BRANCH  VARCHAR(300),
                                    COUNTRY  VARCHAR(300),
                                    SALESREP_ID  VARCHAR(300),
                                    COMM  VARCHAR(300),
                                    TRX_CLASS  VARCHAR(300),
                                    TAXABLE_VALUE VARCHAR(300),
                                    TAX_INVOICE_NUM  VARCHAR(300),
                                    RETURN_REASON_CODE  VARCHAR(300),
                                    RETURN_ORDER_NUM  VARCHAR(300),
                                    RETURN_INVOICE_NUM  VARCHAR(300),
                                    TAX_INVOICE_DATE VARCHAR(300),
                                    TRX_ID  VARCHAR(300),
                                    TRX_LINE_ID  VARCHAR(300),
                                    ORG_ID VARCHAR(300),
                                    SUPPLIER_GST_NUMBER VARCHAR(300),
                                    SUPPLIER_PAN_NUM VARCHAR(300),
                                    CUSTOMER_GST_NUM VARCHAR(300),
                                    CUSTOMER_PAN_NUM VARCHAR(300),
                                    CGST  VARCHAR(300),
                                    CGST_RATE VARCHAR(300),
                                    SGST  VARCHAR(300),
                                    SGST_RATE VARCHAR(300),
                                    IGST VARCHAR(300),
                                    IGST_RATE VARCHAR(300),
                                    CURRENCY_CONVERSION_RATE VARCHAR(300),
                                    REGIME_CODE VARCHAR(300),
                                    GST_EVENT_CLASS_CODE VARCHAR(300),
                                    GST_ENTITY_CODE VARCHAR(300),
                                    DET_FACTOR_ID VARCHAR(300),
                                    SUPP_STATE VARCHAR(300),
                                    BILL_STATE VARCHAR(300),
                                    FREIGHT VARCHAR(300),
                                    INSURANCE VARCHAR(300),
                                    PACKING VARCHAR(300),
                                    TCS VARCHAR(300),
                                    SALES_PERSON VARCHAR(300),
                                    ORDER_CLASS VARCHAR(300),
                                    MIS_CAT1 VARCHAR(300),
                                    MIS_CAT2 VARCHAR(300),
                                    HSN_SAC VARCHAR(300),
                                    ADDRESSEE VARCHAR(300),
                                    TAX_CATEGORY_NAME VARCHAR(300),
                                    CREDIT_MEMO_NUM VARCHAR(300),
                                    CREDIT_MEMO_DATE VARCHAR(300));"""
                cursor.execute(create_statement)
                connection.commit()
                print("Table created successfully in PostgreSQL ")
                return JsonResponse({"Message": f"Table  {TABLE_NAME} Created "})
            except Exception as e:
                return JsonResponse({"Error": e})

        elif table_type == 'insert':
            print(table_type,'ddddddddddddddddddddddddd')
            try:
                sql_stat = f"""INSERT INTO {TABLE_NAME} (EXCHANGE_RATE,
                BUSINESS_UNIT,
                BUSINESS_LINE,
                EVENT_CLASS_CODE,
                ENTITY_CODE,
                DEL_ORG_ID,
                DELIVERY_DETAIL_ID,
                CONSIGNEE_NAME,
                BILL_TO_SITE_USE_ID,
                SHIP_TO_SITE_USE_ID,
                RAC_BILL_TO_CUSTOMER_NAME,
                CUST_ID,
                RAA_BILL_TO_CONCAT_ADDRESS,
                RAA_BILL_TO_POSTAL_CODE,
                RAA_BILL_TO_STATE,
                ORDERED_DATE,
                SHIP_TIME,
                TRX_DATE,
                TERMS,
                CUST_PO_NUMBER,
                PROJ,
                CUSTPODATE,
                DELIVERY_ID,
                OA_NO,
                ORDER_TYPE,
                CUR,
                NET,
                GROSS,
                GROSS_WEIGHT,
                HEADER_ID,
                SP_INS,
                VOLUME,
                RAT_TERM_NAME,
                FOB,
                GST_DATE,
                GST_TIME,
                INVENTORY_ITEM_ID,
                ITEM_CODE,
                DESCRIPTION,
                UNIT_CODE,
                LINE_NUMBER,
                QUANTITY,
                UNIT_PRICE ,
                CONVERSION_RATE,
                WAYBILL,
                TRX_NUMBER,
                REVENUE_AMOUNT,
                REV_UNIT,
                REV_ACCOUNT,
                REV_ACCT_DESC,
                SHIPPING_ORG,
                CUSTOMER_NUMBER,
                SHIP_CUSTOMER,
                SHIP_CUST_GSTN,
                SHIP_CUST_STATE,
                CUSTOMER_CLASS_CODE,
                CUSTOMER_CATEGORY_CODE,
                DOM_IBD,
                ZONE,
                REGION,
                BRANCH,
                COUNTRY,
                SALESREP_ID,
                COMM,
                TRX_CLASS,
                TAXABLE_VALUE,
                TAX_INVOICE_NUM,
                RETURN_REASON_CODE,
                RETURN_ORDER_NUM,
                RETURN_INVOICE_NUM,
                TAX_INVOICE_DATE,
                TRX_ID,
                TRX_LINE_ID,
                ORG_ID,
                SUPPLIER_GST_NUMBER,
                SUPPLIER_PAN_NUM,
                CUSTOMER_GST_NUM,
                CUSTOMER_PAN_NUM,
                CGST,
                CGST_RATE,
                SGST,
                SGST_RATE,
                IGST,
                IGST_RATE,
                CURRENCY_CONVERSION_RATE,
                REGIME_CODE,
                GST_EVENT_CLASS_CODE,
                GST_ENTITY_CODE,
                DET_FACTOR_ID,
                SUPP_STATE,
                BILL_STATE,
                FREIGHT,
                INSURANCE,
                PACKING,
                TCS,
                SALES_PERSON,
                ORDER_CLASS,
                MIS_CAT1,
                MIS_CAT2,
                HSN_SAC,
                ADDRESSEE,
                TAX_CATEGORY_NAME,
                CREDIT_MEMO_NUM,
                CREDIT_MEMO_DATE) VALUES {res};"""

                cursor.execute(sql_stat)
                connection.commit()
                print(connection, 'ddddddddddddddeee3333333333333333333333333333')
                return JsonResponse({"Message": f"Data inserted in {TABLE_NAME} Successfully"})
                # return HttpResponse("Message")
            except Exception as e:
                print(e,'ddddddddddddddddddddddddddddd')
                return JsonResponse({"Error": e})
        elif table_type == 'replace':
            try:
                drop_table = f"DROP TABLE {REPLACE_TABLE_NAME} ;"
                cursor.execute(drop_table)
                connection.commit()
                sql_statement =f""" CREATE TABLE {TABLE_NAME} (EXCHANGE_RATE VARCHAR(300),
                                       BUSINESS_UNIT VARCHAR(300),
                                       BUSINESS_LINE VARCHAR(300),
                                       EVENT_CLASS_CODE VARCHAR(300),
                                       ENTITY_CODE VARCHAR(300),
                                       DEL_ORG_ID VARCHAR(300),
                                        DELIVERY_DETAIL_ID VARCHAR(300),
                                        CONSIGNEE_NAME  VARCHAR(300),
                                        BILL_TO_SITE_USE_ID  VARCHAR(300),
                                        SHIP_TO_SITE_USE_ID  VARCHAR(300),
                                        RAC_BILL_TO_CUSTOMER_NAME  VARCHAR(300),
                                        CUST_ID  VARCHAR(300),
                                        RAA_BILL_TO_CONCAT_ADDRESS  VARCHAR(1200),
                                        RAA_BILL_TO_POSTAL_CODE  VARCHAR(300),
                                        RAA_BILL_TO_STATE  VARCHAR(300),
                                        ORDERED_DATE  VARCHAR(300),
                                        SHIP_TIME  VARCHAR(300),
                                        TRX_DATE  VARCHAR(300),
                                        TERMS  VARCHAR(300),
                                        CUST_PO_NUMBER  VARCHAR(300),
                                        PROJ VARCHAR(300),
                                        CUSTPODATE  VARCHAR(300),
                                        DELIVERY_ID  VARCHAR(300),
                                        OA_NO  VARCHAR(300),
                                        ORDER_TYPE  VARCHAR(300),
                                        CUR  VARCHAR(300),
                                        NET VARCHAR(300),
                                        GROSS  VARCHAR(300),
                                        GROSS_WEIGHT  VARCHAR(300),
                                        HEADER_ID  VARCHAR(300),
                                        SP_INS  VARCHAR(300),
                                        VOLUME  VARCHAR(300),
                                        RAT_TERM_NAME  VARCHAR(300),
                                        FOB  VARCHAR(300),
                                        GST_DATE VARCHAR(300),
                                        GST_TIME   VARCHAR(300),
                                        INVENTORY_ITEM_ID VARCHAR(300),
                                        ITEM_CODE VARCHAR(300),
                                        DESCRIPTION VARCHAR(300),
                                        UNIT_CODE VARCHAR(300),
                                        LINE_NUMBER VARCHAR(300),
                                        QUANTITY VARCHAR(300),
                                        UNIT_PRICE  VARCHAR(300) ,
                                        CONVERSION_RATE  VARCHAR(300),
                                        WAYBILL  VARCHAR(300),
                                        TRX_NUMBER  VARCHAR(300),
                                        REVENUE_AMOUNT VARCHAR(300),
                                        REV_UNIT  VARCHAR(300),
                                        REV_ACCOUNT  VARCHAR(300),
                                        REV_ACCT_DESC  VARCHAR(300),
                                        SHIPPING_ORG  VARCHAR(300),
                                        CUSTOMER_NUMBER  VARCHAR(300),
                                        SHIP_CUSTOMER  VARCHAR(300),
                                        SHIP_CUST_GSTN  VARCHAR(300),
                                        SHIP_CUST_STATE  VARCHAR(300),
                                        CUSTOMER_CLASS_CODE  VARCHAR(300),
                                        CUSTOMER_CATEGORY_CODE  VARCHAR(300),
                                        DOM_IBD  VARCHAR(300),
                                        ZONE  VARCHAR(300),
                                        REGION  VARCHAR(300),
                                        BRANCH  VARCHAR(300),
                                        COUNTRY  VARCHAR(300),
                                        SALESREP_ID  VARCHAR(300),
                                        COMM  VARCHAR(300),
                                        TRX_CLASS  VARCHAR(300),
                                        TAXABLE_VALUE VARCHAR(300),
                                        TAX_INVOICE_NUM  VARCHAR(300),
                                        RETURN_REASON_CODE  VARCHAR(300),
                                        RETURN_ORDER_NUM  VARCHAR(300),
                                        RETURN_INVOICE_NUM  VARCHAR(300),
                                        TAX_INVOICE_DATE VARCHAR(300),
                                        TRX_ID  VARCHAR(300),
                                        TRX_LINE_ID  VARCHAR(300),
                                        ORG_ID VARCHAR(300),
                                        SUPPLIER_GST_NUMBER VARCHAR(300),
                                        SUPPLIER_PAN_NUM VARCHAR(300),
                                        CUSTOMER_GST_NUM VARCHAR(300),
                                        CUSTOMER_PAN_NUM VARCHAR(300),
                                        CGST  VARCHAR(300),
                                        CGST_RATE VARCHAR(300),
                                        SGST  VARCHAR(300),
                                        SGST_RATE VARCHAR(300),
                                        IGST VARCHAR(300),
                                        IGST_RATE VARCHAR(300),
                                        CURRENCY_CONVERSION_RATE VARCHAR(300),
                                        REGIME_CODE VARCHAR(300),
                                        GST_EVENT_CLASS_CODE VARCHAR(300),
                                        GST_ENTITY_CODE VARCHAR(300),
                                        DET_FACTOR_ID VARCHAR(300),
                                        SUPP_STATE VARCHAR(300),
                                        BILL_STATE VARCHAR(300),
                                        FREIGHT VARCHAR(300),
                                        INSURANCE VARCHAR(300),
                                        PACKING VARCHAR(300),
                                        TCS VARCHAR(300),
                                        SALES_PERSON VARCHAR(300),
                                        ORDER_CLASS VARCHAR(300),
                                        MIS_CAT1 VARCHAR(300),
                                        MIS_CAT2 VARCHAR(300),
                                        HSN_SAC VARCHAR(300),
                                        ADDRESSEE VARCHAR(300),
                                        TAX_CATEGORY_NAME VARCHAR(300),
                                        CREDIT_MEMO_NUM VARCHAR(300),
                                        CREDIT_MEMO_DATE VARCHAR(300));"""
                print(sql_statement)
                cursor.execute(sql_statement)
                connection.commit()
                print("Table created successfully in PostgreSQL ")
                sql_stat = f"""INSERT INTO {TABLE_NAME} (EXCHANGE_RATE,
                BUSINESS_UNIT,
                BUSINESS_LINE,
                EVENT_CLASS_CODE,
                ENTITY_CODE,
                DEL_ORG_ID,
                DELIVERY_DETAIL_ID,
                CONSIGNEE_NAME,
                BILL_TO_SITE_USE_ID,
                SHIP_TO_SITE_USE_ID,
                RAC_BILL_TO_CUSTOMER_NAME,
                CUST_ID,
                RAA_BILL_TO_CONCAT_ADDRESS,
                RAA_BILL_TO_POSTAL_CODE,
                RAA_BILL_TO_STATE,
                ORDERED_DATE,
                SHIP_TIME,
                TRX_DATE,
                TERMS,
                CUST_PO_NUMBER,
                PROJ,
                CUSTPODATE,
                DELIVERY_ID,
                OA_NO,
                ORDER_TYPE,
                CUR,
                NET,
                GROSS,
                GROSS_WEIGHT,
                HEADER_ID,
                SP_INS,
                VOLUME,
                RAT_TERM_NAME,
                FOB,
                GST_DATE,
                GST_TIME,
                INVENTORY_ITEM_ID,
                ITEM_CODE,
                DESCRIPTION,
                UNIT_CODE,
                LINE_NUMBER,
                QUANTITY,
                UNIT_PRICE ,
                CONVERSION_RATE,
                WAYBILL,
                TRX_NUMBER,
                REVENUE_AMOUNT,
                REV_UNIT,
                REV_ACCOUNT,
                REV_ACCT_DESC,
                SHIPPING_ORG,
                CUSTOMER_NUMBER,
                SHIP_CUSTOMER,
                SHIP_CUST_GSTN,
                SHIP_CUST_STATE,
                CUSTOMER_CLASS_CODE,
                CUSTOMER_CATEGORY_CODE,
                DOM_IBD,
                ZONE,
                REGION,
                BRANCH,
                COUNTRY,
                SALESREP_ID,
                COMM,
                TRX_CLASS,
                TAXABLE_VALUE,
                TAX_INVOICE_NUM,
                RETURN_REASON_CODE,
                RETURN_ORDER_NUM,
                RETURN_INVOICE_NUM,
                TAX_INVOICE_DATE,
                TRX_ID,
                TRX_LINE_ID,
                ORG_ID,
                SUPPLIER_GST_NUMBER,
                SUPPLIER_PAN_NUM,
                CUSTOMER_GST_NUM,
                CUSTOMER_PAN_NUM,
                CGST,
                CGST_RATE,
                SGST,
                SGST_RATE,
                IGST,
                IGST_RATE,
                CURRENCY_CONVERSION_RATE,
                REGIME_CODE,
                GST_EVENT_CLASS_CODE,
                GST_ENTITY_CODE,
                DET_FACTOR_ID,
                SUPP_STATE,
                BILL_STATE,
                FREIGHT,
                INSURANCE,
                PACKING,
                TCS,
                SALES_PERSON,
                ORDER_CLASS,
                MIS_CAT1,
                MIS_CAT2,
                HSN_SAC,
                ADDRESSEE,
                TAX_CATEGORY_NAME,
                CREDIT_MEMO_NUM,
                CREDIT_MEMO_DATE)
                                            VALUES {res};"""
                cursor.execute(sql_stat)
                connection.commit()
                print("Data inserted successfully in Table !!")
                return JsonResponse({"Message": f"Data Replaced from {REPLACE_TABLE_NAME} &"
                                                f"Created and Inserted data in {TABLE_NAME} Successfully"})
            except Exception as e:
                return JsonResponse({"Error": e})
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating PostgreSQL table", error)
    context = {
        "newData": newData
    }
    return render(request, 'app/app/dump_report.html')


def dump_download_report_parameter(request):
    '''
    Front view  to download the report
    :param request:
    :return:
    '''
    form = DumpDownloadForm(request.POST or None)
    if form.is_valid():
        data = form.save(commit=False)
        report_type = form.cleaned_data['report_type']
        business_line = form.cleaned_data['business_line']
        business_unit = form.cleaned_data['business_unit']
        shipping_org = form.cleaned_data['shipping_org']
        from_date = form.cleaned_data['from_date']
        to_date = form.cleaned_data['to_date']
        unit = form.cleaned_data['unit']
        sales_account = form.cleaned_data['sales_account']
        form.save()
        return redirect('')
    else:
        print(form.errors)
    return render(request, 'app/app/dump_report_download_parameter.html', {'form': form})


@api_view(['POST'])
def download_dump_report(request):
    '''
    Download the report from postgres database
    :param request:
    :return:
    '''
    data = request.data
    report_type = data['report_type']
    print(report_type)
    cursor = connection.cursor()
    sql_statement = f'''SELECT * FROM  public.{TABLE_NAME}'''
    cursor.execute(sql_statement)
    row_data = cursor.fetchall()
    output = BytesIO()
    if report_type == 'excel':
        workbook = xlsxwriter.Workbook(output, {'constant_memory': True})
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})
        headings = ['EXCHANGE_RATE', 'BUSINESS_UNIT', 'BUSINESS_LINE', 'EVENT_CLASS_CODE', 'ENTITY_CODE', 'DEL_ORG_ID',
            'DELIVERY_DETAIL_ID', 'CONSIGNEE_NAME', 'BILL_TO_SITE_USE_ID', 'SHIP_TO_SITE_USE_ID', 'RAC_BILL_TO_CUSTOMER_NAME',
            'CUST_ID', 'RAA_BILL_TO_CONCAT_ADDRESS', 'RAA_BILL_TO_POSTAL_CODE', 'RAA_BILL_TO_STATE',
            'ORDERED_DATE', 'SHIP_TIME', 'TRX_DATE',  'TERMS', 'CUST_PO_NUMBER', 'PROJ',  'CUSTPODATE', 'DELIVERY_ID',
            'OA_NO',
            'ORDER_TYPE',
            'CUR',
            'NET',
            'GROSS',
            'GROSS_WEIGHT',
            'HEADER_ID',
            'SP_INS',
            'VOLUME',
            'RAT_TERM_NAME',
            'FOB',
            'GST_DATE',
            'GST_TIME',
            'INVENTORY_ITEM_ID',
            'ITEM_CODE',
            'DESCRIPTION',
            'UNIT_CODE',
            'LINE_NUMBER',
            'QUANTITY',
            'UNIT_PRICE' ,
            'CONVERSION_RATE',
            'WAYBILL',
            'TRX_NUMBER',
            'REVENUE_AMOUNT',
            'REV_UNIT',
            'REV_ACCOUNT',
            'REV_ACCT_DESC',
            'SHIPPING_ORG',
            'CUSTOMER_NUMBER',
            'SHIP_CUSTOMER',
            'SHIP_CUST_GSTN',
            'SHIP_CUST_STATE',
            'CUSTOMER_CLASS_CODE',
            'CUSTOMER_CATEGORY_CODE',
            'DOM_IBD',
            'ZONE',
            'REGION',
            'BRANCH',
            'COUNTRY',
            'SALESREP_ID',
            'COMM',
            'TRX_CLASS',
            'TAXABLE_VALUE',
            'TAX_INVOICE_NUM',
            'RETURN_REASON_CODE',
            'RETURN_ORDER_NUM',
            'RETURN_INVOICE_NUM',
            'TAX_INVOICE_DATE',
            'TRX_ID',
            'TRX_LINE_ID',
            'ORG_ID',
            'SUPPLIER_GST_NUMBER',
            'SUPPLIER_PAN_NUM',
            'CUSTOMER_GST_NUM',
            'CUSTOMER_PAN_NUM',
            'CGST',
            'CGST_RATE',
            'SGST',
            'SGST_RATE',
            'IGST',
            'IGST_RATE',
            'CURRENCY_CONVERSION_RATE',
            'REGIME_CODE',
            'GST_EVENT_CLASS_CODE',
            'GST_ENTITY_CODE',
            'DET_FACTOR_ID',
            'SUPP_STATE',
            'BILL_STATE',
            'FREIGHT',
            'INSURANCE',
            'PACKING',
            'TCS',
            'SALES_PERSON',
            'ORDER_CLASS',
            'MIS_CAT1',
            'MIS_CAT2',
            'HSN_SAC',
            'ADDRESSEE',
            'TAX_CATEGORY_NAME',
            'CREDIT_MEMO_NUM',
            'CREDIT_MEMO_DATE']
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